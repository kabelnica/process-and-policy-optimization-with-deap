# CI/CD cauruļvada optimizācija izmantojot ģenētisko algoritmu
# Versija: 1.0
# Autors: Kaspars Ābelnīca
# Modelis izstrādāts balstoties uz OpenAI ChatGPT 4.5 izveidotu šablonu un pielāgots izmantojot DEAP dokumentāciju
# DEAP dokumentācija: https://deap.readthedocs.io/en/master/

import time, requests, random, math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from datetime import datetime
from deap import base, creator, tools

# Mainīgie optimizācijas modelim
warning_policy_count = 10 # Rego brīdinājumu warn[] skaits (patreiz izgūts ar rokām no politiku datnes)
deny_policy_count = 9 # Rego atteiču deny[] skaits (patreiz izgūts ar rokām no politiku datnes)
emp_upper_bound = 220.0 # Augšējā robeža izvietošanas laikam (s) (noteikta empīriski testa infrastruktūrai)
stagnation_counter = 0 # Cik paaudzes nav uzlabojies fitness (algoritms iesprūst)

# Izvēlas pēc cik stagnējošām paaudzēm veicināt mutācijas algortimā
STAGNATION_LIMIT = 3 

# Vardnīca, kas glabā iepriekšējus novērtējumus (kešatmiņa)
evaluation_cache = {}
jenkins_job_count = 0
cache_hit_count = 0

# Fiksē sākuma laiku, lai mērītu skripta izpildes ilgumu
start_time = time.time()

# Iestartē gadījuma skaitļu ģeneratoru rezultātu atkārtošanai
random.seed(5)

# Jenkins API konfigurācija
JENKINS_URL = "http://192.168.56.10:8080"
JOB_NAME = "OPA-gala-modelis"
JENKINS_USER = <JENKINS_USER>
JENKINS_TOKEN = <JENKINS_TOKEN>

# Iespējamie LXC šabloni
OS_OPTIONS = [
    "local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst",
    "local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst",
    "local:vztmpl/ubuntu-25.04-standard_25.04-1.1_amd64.tar.zst",
    "local:vztmpl/alpine-3.21-default_20241217_amd64.tar.xz"
]

# Paroļu šablonu varianti
PSWD_OPTIONS = [
    "pswd123", "password", "SuperStrongAndSecurePassword", "sdf#Dsdgls", "pswd", 
]

# Diska izmēru varianti
DISK_OPTIONS = [
    "4G", "8G", "12G", "16G", "25G"
]

# Atmiņas šablonu varianti
MEMORY_OPTIONS = [
    256, 512, 1024, 2048
]

# Definē daudzkritēriju optimizācijas uzdevumu
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Definēt gēnus (politiku kontroles)
def random_small_count():
    return random.randint(1, 5)

def random_large_count():
    return random.randint(1, 4)

def random_password():
    return random.choice(PSWD_OPTIONS)

def random_memory():
    return random.choice(MEMORY_OPTIONS)

def random_disk():
    return random.choice(DISK_OPTIONS)

def random_bool():
    return bool(random.getrandbits(1))

def random_os():
    return random.choice(OS_OPTIONS)

def random_cpu():
    return random.randint(1, 2)

# DEAP toolbox izveide
toolbox = base.Toolbox()
toolbox.register("large_container_count", random_large_count)
toolbox.register("large_container_password", random_password)
toolbox.register("large_container_unprivileged", random_bool)
toolbox.register("large_container_os", random_os)
toolbox.register("large_container_memory", random_memory)
toolbox.register("large_container_swap", random_memory)
toolbox.register("large_container_disk_size", random_disk)
toolbox.register("large_container_firewall", random_bool)
toolbox.register("small_container_count", random_small_count)
toolbox.register("small_container_password", random_password)
toolbox.register("small_container_unprivileged", random_bool)
toolbox.register("small_container_os", random_os)
toolbox.register("small_container_memory", random_memory)
toolbox.register("small_container_swap", random_memory)
toolbox.register("small_container_disk_size", random_disk)
toolbox.register("small_container_firewall", random_bool)
toolbox.register("small_container_cpu", random_cpu)

toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.large_container_count, toolbox.large_container_password,
                  toolbox.large_container_unprivileged, toolbox.large_container_os,
                  toolbox.large_container_memory, toolbox.large_container_swap, 
                  toolbox.large_container_disk_size, toolbox.large_container_firewall, 
                  toolbox.small_container_count, toolbox.small_container_password,
                  toolbox.small_container_unprivileged, toolbox.small_container_os,
                  toolbox.small_container_memory, toolbox.small_container_swap, 
                  toolbox.small_container_disk_size, toolbox.small_container_firewall, toolbox.small_container_cpu), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Krustošanās (crossover) funkcija pielāgota problēmai
def mateCompliance(individual1, individual2):
    for i in range(len(individual1)):
        if random.random() <= 0.5:
            individual1[i], individual2[i] = individual2[i], individual1[i]
    return individual1, individual2

# Mutācijas funkcija pielāgot problēmai
def mutCompliance(individual):
    # large_container_count 
    if random.random() <= 0.4:
        individual[0] = random_large_count()

    #  large_container_password
    if random.random() <= 0.4:
        individual[1] = random_password()

    # large_container_unprivileged (pretējs bool)
    if random.random() <= 0.4:
        individual[2] = not individual[2]

    # large_container_os
    if random.random() <= 0.4:
        individual[3] = random_os()

    # large_container_memory
    if random.random() <= 0.4:
        individual[4] = random_memory()

    # large_container_swap
    if random.random() <= 0.4:
        individual[5] = random_memory()

    # large_container_disk_size 
    if random.random() <= 0.4:
        individual[6] = random_disk()

    # large_container_firewall (pretējs bool)
    if random.random() <= 0.4:
        individual[7] = not individual[7]

    # small_container_count 
    if random.random() <= 0.4:
        individual[8] = random_small_count()

    #  small_container_password
    if random.random() <= 0.4:
        individual[9] = random_password()

    # small_container_unprivileged (pretējs bool)
    if random.random() <= 0.4:
        individual[10] = not individual[10]

    # small_container_os
    if random.random() <= 0.4:
        individual[11] = random_os()

    # small_container_memory
    if random.random() <= 0.4:
        individual[12] = random_memory()

    # small_container_swap
    if random.random() <= 0.4:
        individual[13] = random_memory()

    # small_container_disk_size 
    if random.random() <= 0.4:
        individual[14] = random_disk()

    # small_container_firewall (pretējs bool)
    if random.random() <= 0.4:
        individual[15] = not individual[15]

    # small_container_cpu (pretējs bool)
    if random.random() <= 0.4:
        individual[16] = random_cpu()      

    return individual

# Funkcija, lai saglabātu indivīda gēnu izvēles, kā atslēgu kešam
def individualKey(individual):
    return tuple(individual)

# Fitness novērtēšanas funkcija
def evalCompliance(individual):
    global cache_hit_count
    global jenkins_job_count

    # Pirms vērsties pie Jenkins, pārbauda kešatmiņu
    key = individualKey(individual)
    if key in evaluation_cache:
        cache_hit_count += 1
        return evaluation_cache[key]
    
    # Sadalām indivīdu mainīgajos, ko nodot Jenkins
    (large_count, large_password, large_privileged, large_os_template, large_memory, 
    large_swap, large_disk_size, large_firewall, small_count, small_password, small_privileged,
     small_os_template, small_memory, small_swap, small_disk_size, small_firewall, small_cpu) = individual

    # Paremetri, ko nodod Jenkins
    params = {
        "LARGE_CONTAINER_COUNT": large_count,
        "LARGE_CONTAINER_PASSWORD": large_password,
        "LARGE_CONTAINER_UNPRIVILEGED": str(large_privileged).lower(),
        "LARGE_CONTAINER_OS": large_os_template,
        "LARGE_CONTAINER_MEMORY": large_memory,
        "LARGE_CONTAINER_SWAP": large_swap,
        "LARGE_CONTAINER_DISK_SIZE": large_disk_size,
        "LARGE_CONTAINER_FIREWALL": str(large_firewall).lower(),
        "SMALL_CONTAINER_COUNT": small_count,
        "SMALL_CONTAINER_PASSWORD": small_password,
        "SMALL_CONTAINER_UNPRIVILEGED": str(small_privileged).lower(),
        "SMALL_CONTAINER_OS": small_os_template,
        "SMALL_CONTAINER_MEMORY": small_memory,
        "SMALL_CONTAINER_SWAP": small_swap,
        "SMALL_CONTAINER_DISK_SIZE": small_disk_size,
        "SMALL_CONTAINER_FIREWALL": str(small_firewall).lower(),
        "SMALL_CONTAINER_CPU": small_cpu
    }

    # Izsaukt cauruļvadu
    build_url = f"{JENKINS_URL}/job/{JOB_NAME}/buildWithParameters"
    auth = (JENKINS_USER, JENKINS_TOKEN)
    response = requests.post(build_url, auth=auth, params=params)
    jenkins_job_count += 1

    # Noraksta indivīdu, ja Jenkins neizpildījās, kā sliktāko iespējamo fit vērtību
    if response.status_code not in [200, 201]:
        print("Nevarēja izpildīt Jenkins cauruļvadu!")
        return (0, 1.0)

    # Gaida atbildi no Jenkins par darba sākumu
    queue_url = response.headers["Location"] + "api/json"
    build_number = None
    while build_number is None:
        queue_resp = requests.get(queue_url, auth=auth).json()
        build_number = queue_resp.get("executable", {}).get("number")
        time.sleep(2)

    # Gaida kamēr izpildās cauruļvads
    build_status_url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/api/json"
    building = True
    while building:
        build_resp = requests.get(build_status_url, auth=auth).json()
        building = build_resp["building"]
        time.sleep(5)

    # Savāc artefaktu (Terraform darbības laiku)
    artifacts_url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/artifact/deploy_time.txt"
    artifacts_output = requests.get(artifacts_url, auth=auth)
    
    # Ja izvietošanas laiks ir nepareizs datu tips, tad noraksta indivīdu ar sliktāto fit vērtību
    try:
        deploy_time_sec = float(artifacts_output.text)
    except ValueError:
        compliance_score = 0
        normalized_time  = 1.0
        print(f"KĻŪDA: izvietošanas laiks #{build_number} laidienam nav skaitlis!")
        return compliance_score, normalized_time

    # Logaritmiski mērogo laiku, lai tas nedominētu rezultātus
    normalized_time = math.log(1 + deploy_time_sec) / math.log(1 + emp_upper_bound)

    # Izgūst Jenkins konsoles žurnālu
    console_url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/consoleText"
    console_output = requests.get(console_url, auth=auth).text

    # Pārbaude uz politiku nosacījumiem no Jenkins konsoles
    violation_score = 0
    for line in console_output.splitlines():
        if "WARN - plan.json" in line:
            violation_score += 1
        elif "FAIL - plan.json" in line:
            violation_score += 4 # Pieņem, ka deny[] ir četras reizes sliktāki nekā warn[]

    # Aprēķina cik labi indivīds ievēro politikas
    compliance_score = 1 - (violation_score/(warning_policy_count+(deny_policy_count*4)))

    evaluation_cache[key] = (compliance_score, normalized_time)
    return compliance_score, normalized_time

# Ģenētiskā algoritma konfigurācija
# Evolūcijas stratēģija
toolbox.register("evaluate", evalCompliance)
toolbox.register("mate", mateCompliance)
toolbox.register("mutate", mutCompliance)
toolbox.register("select", tools.selNSGA2)

# Izpilda ģenētisko algortimu noteiktu iterāciju skaitu
population = toolbox.population(n=12)
NGEN = 25

# Masīvi modelēšanas rezultātu glabāšanai
model_values = []
best_fitness_values = []
last_best_fitness = None

# Izpilda modeli NGEN pauaudzēm
for gen in range(1, NGEN + 1):

    # Definē, elites indivīdu skaitu (ceļ, kad modelis ir jau kādu laiku darbināts)
    if gen<=5:
        ELITES_N = 1
    else:
        ELITES_N = 3

    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    # Pēcnācēju atlase
    offspring = toolbox.select(population, len(population) - ELITES_N)
    offspring = list(map(toolbox.clone, offspring))

    # Krustošanās (crossover)
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() <= 0.5:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    # Pirms mutācijas veic stagnācijas pārbaudi (algoritms ir iesprūdis)
    best_ind_premutation = tools.selBest(population, 1)[0]
    current_fitness = best_ind_premutation.fitness.values
    if last_best_fitness == current_fitness:
        stagnation_counter += 1
    else:
        stagnation_counter = 0
    last_best_fitness = current_fitness

    # Ja ilgstoši stagnē, tad veicina mutācijas algoritmā
    if stagnation_counter < STAGNATION_LIMIT:
        mutation_rate = 0.3
    else: 
        mutation_rate = 0.7

    # Mutācijas
    for mutant in offspring:
        if random.random() <= mutation_rate:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Novērtē jaunos indivīdus
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Izveido jauno populāciju (ar eliti)
    elites = tools.selBest(population, ELITES_N)
    population[:] = offspring + elites

    # Identificē labāko indivīdu rezultātiem
    best_ind = tools.selBest(population, 1)[0]
    model_values.append(best_ind)
    best_fitness_values.append(best_ind.fitness.values)
    print(f"Paaudze {gen}: Labākais indivīds = {best_ind}, Fit = {best_ind.fitness.values}")

# Atgriež kopējo izpildes laiku
print(f"Modeļa izpildes laiks: {round((time.time() - start_time), 3)} sekundes")
print(f"Jenkins cauruļvads ir izsaukts {jenkins_job_count} reizes")
print(f"Kešatmiņa izlaida cauruļvada izpildi {cache_hit_count} reizes")

# Izgūst modelēšanas rezultātus
compliance_scores, normalized_times = zip(*best_fitness_values)
individual_configurations = [str(ind) for ind in model_values]

# Saglabā modeļa rezultātus kā DataFrame CSV datnē 
df = pd.DataFrame({
    "Paaudze": list(range(1, len(model_values) + 1)),
    "Labākais indivīds": individual_configurations,
    "Politiku atbilstība": compliance_scores,
    "Izvietošanas laiks (normalizēts)": normalized_times
})
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
df.to_csv(f"results/model_results_{timestamp}.csv", index=False)

# Vizualizē fitness funkcijas (piemērs no DEAP)
fig, ax1 = plt.subplots()
line1 = ax1.plot(compliance_scores, "b-", label="max fitness")
ax1.set_xlabel("Paaudze")
ax1.set_ylabel("Politiku atbilstība", color="b")
for tl in ax1.get_yticklabels():
    tl.set_color("b")
ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))    

ax2 = ax1.twinx()
line2 = ax2.plot(normalized_times, "r-", label="Vidējais laiks")
ax2.set_ylabel("Konfigurācijas laiks", color="r")
for tl in ax2.get_yticklabels():
    tl.set_color("r")

# Saglabā un parāda lietotājam
plt.savefig(f"results/model_results_{timestamp}.png")
plt.show()

# Sakārto visus rezultātu punktus, lai noteiktu Pareto robežu
points = sorted(zip(normalized_times, compliance_scores, range(1, len(normalized_times)+1)))

# Definē mainīgos Pareto robežas identificēšanai
pareto_front = []

# Identificēt kuri punkti veido Pareto robežu
for i, (x1, y1, _) in enumerate(points):
    dominated = False
    for j, (x2, y2, _) in enumerate(points):
        if i != j and x2 <= x1 and y2 >= y1 and (x2 < x1 or y2 > y1):
            dominated = True
            break
    if not dominated:
        pareto_front.append((x1, y1))

# Punkti caur kuriem izvilkt Pareto robežu
pareto_x, pareto_y = zip(*pareto_front)

plt.scatter(normalized_times, compliance_scores, label="Konfigurācijas")
plt.plot(pareto_x, pareto_y, linestyle="--", marker="o", label="Pareto robeža")

plt.xlabel("Izvietošanas laiks (Min)")
plt.ylabel("Politiku atbilstība (Max)")
plt.title("Pareto robeža")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Saglabā un parāda lietotājam
plt.savefig(F"results/pareto_front_{timestamp}.png")
plt.show()

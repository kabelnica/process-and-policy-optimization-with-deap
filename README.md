# Infrastruktūras izvietošanas procesa optimizācijas algoritms

## Tehniskās prasības
Lai izvietotu modeli uz resursdatora bez modifikācijām, lietotājam ir nepieciešams uzstādīt:
- Vagrant 2.4.5+
- VirtualBox 7.1.8+
- Python 3.12+ ar DEAP bibliotēku (vai Anaconda)
- Proxmox VE hipervizoru

## Proxmox VE
Proxmox VE hipervizoru ir nepieciešams manuāli uzstādīt uz tam īpaši atvēlētas infrastruktūras. To ir ieteicams izvietot uz fiziskas iekārts, bet var izmantot arī virtuālo mašīnu, ja procesors atbalsta *nested virtualization*.
Instalācijas procesā ir ieteicams sekot [Proxmox dokumentācijai](https://www.proxmox.com/en/products/proxmox-virtual-environment/get-started).

Optimizācijas modelis sagaida sekojošus LXC šablonus uz Proxmox VE:
- local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst
- local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst
- local:vztmpl/ubuntu-25.04-standard_25.04-1.1_amd64.tar.zst
- alpine-3.21-default_20241217_amd64.tar.xz

Šablonus Proxmox var lejuplādēt ar `pveam download` komandu

## Vagrant nfrastruktūras izveide
No repozitorija galvenā kataloga infrastruktūru ir iespējams izvietot ar komandu `vagrant up`. Pēc veiksmīgas Vagrant izpildes, VirtualBox ir jāparādās Jenkins un Terraform serveriem.
Virtuālajām mašīnām ir iespējams piekļūt ar `vagrant ssh jenkins` un `vagrant ssh terraform`. 
Lai nodrošinātu Jenkins saziņu ar Terraform, uz Jenkins servera ir nepieciešams izveidot SSH atslēgu ar komandu `ssh-keygen`, kuras publisko atslēgu (id_rsa.pub) ir nepieciešams pievienot uz Terraform servera `.ssh/authorized_keys` sarakstam:
```
ssh-rsa <PUBLIC_KEY> vagrant@jenkins
```

## Jenkins serveris
Pēc Vagrant izpildes ir nepieciešams doties uz Jenkins tīmekļa saskarni, lai pabeigtu Jenkins instalāciju.
Jenkins URL: http://192.168.56.10:8080/
Pēc instalācijas nepieciešams veikt sekojošos soļus
- Pievienot SSH Agent spraudni
- Izveidot [jaunu API token](https://plugins.jenkins.io/ssh-agent/), **jenkins-tf-key**, kas satur vagrant lietotāja privāto atslēgu (id_rsa).
- Jāizveido Jenkins API token (Dashboard -> User -> Security), kura vertību jāpievieno optimizācijas modeļa pirmkodam `optimization_model.py`

Pēc Jenkins konfigurācijas ir jāizveido jauns cauruļvads 'OPA-gala-modelis', skripta daļā iekļaujot **Jenkinsfile** datnes saturu.

Sīkāk skatīt [Jenkins dokumentāciju](https://www.jenkins.io/doc/).

## Terraform serveris
Terraform servera veiksmīgu instalāciju ir iespējams pārbaudīt, pieslēdzieties virtuālajai mašīnai caur komandrindu un izpildiet kommandu:
```
terraform -v 
```
Terraform servera lietotāja katalogā ir izveidots katalogs **/terraform-proxmox-test**, kuras mainīgo datnē **variables.tf** ir jāiekļauj Proxmox VE lietotāja informācija. Proxmox lietotājam ir jābūt ar tiesībām izveidot un dzēst virtuālās mašīnas, lai Terraform varētu strādāt.

## DEAP optimizācijas algoritms
Optimizācijas algoritms jau ir sakonfigurēts ar darbā apskatītajiem modelēšanas parametrim.. Lai izpildītu Python skriptu ir nepieciešams vienīgi pievienot Jenkins lietotāja API informāciju.
Modelēšanas rezultāti ir saglabāti **/results** katalogā. Tajā arī glabājas modelēšanas rezultātu piemērs, kas apskatīts darbā.



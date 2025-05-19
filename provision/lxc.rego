# Rego politikas cauruļvada izveidotajiem LXC
# Versija: 1.0
# Autors: Kaspars Ābelnīca
# Modelis izstrādāts balstoties uz OpenAI ChatGPT 4.5 izveidotu šablonu un pielāgots izmantojot OPA dokumentāciju
# OPA Rego dokumentācija: https://www.openpolicyagent.org/docs/latest/policy-language/

package main

default allow = true

# Parbaudes uz Terraform parametru vertibam

# Lielie konteineri
warn["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.10) large_container_count should not exceed 2"] {
    to_number(input.variables.large_container_count.value) > 2
}

deny["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.10) large_container_count may not exceed 3"] {
    to_number(input.variables.large_container_count.value) > 3
}

warn["(COBIT 2019: DSS05.03, ISO 27001:2022: A.8.2) large_container_password must be at least 12 characters long"] {
    count(input.variables.large_container_password.value) < 12
}

deny["(COBIT 2019: DSS05.03, ISO 27001:2022: A.8.2) large_container_password must not be a common dictionary password"] {
    common_passwords := {"password", "pswd", "pswd123", "parole"}
    lower(input.variables.large_container_password.value) == common_passwords[_]
}

warn["(COBIT 2019: DSS05.02, ISO 27001:2022: A.8.2) large containers should run as unprivileged"] {
    input.variables.large_container_unprivileged.value != "true"
}

deny["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.10) large_container_os must be Ubuntu 24.04"] {
    not startswith(lower(input.variables.large_container_os.value), "local:vztmpl/ubuntu-24.04")
}

warn["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.12) large_container_memory should be at least 1024"] {
    to_number(input.variables.large_container_memory.value) < 1024
}

deny["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.30) large_container_memory cannot be less than 512"] {
    to_number(input.variables.large_container_memory.value) < 512
}

warn["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.30) large_container_swap should be greater than 512"] {
    not to_number(input.variables.large_container_swap.value) >= 512
}

deny["(COBIT 2019: DSS01.04, ISO 27001:2022: A.5.30) large_container_disk_size must not be small"] {
    small_disks := {"4G", "8G"}
    input.variables.large_container_disk_size.value == small_disks[_]
}

warn["(COBIT 2019: DSS05.03, ISO 27001:2022: A.8.20) large containers should have a firewall"] {
    input.variables.large_container_firewall.value != "true"
}

# Mazie konteineri
deny["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.10) small_container_count must be at least 3"] {
    to_number(input.variables.small_container_count.value) < 3
}

deny["(COBIT 2019: DSS01.04, ISO 27001:2022: A.5.30) small_container_disk_size must be small"] {
    large_disks := {"12G", "16G", "25G"}
    input.variables.small_container_disk_size.value == large_disks[_]
}

warn["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.30) small_container_memory should not exceed 512"] {
    to_number(input.variables.small_container_memory.value) > 512
}

warn["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.30) small_container_swap should not exceed 256"] {
    to_number(input.variables.small_container_swap.value) > 256
}

warn["(COBIT 2019: DSS05.02, ISO 27001:2022: A.8.2) small containers should run as unprivileged"] {
    input.variables.small_container_unprivileged.value != "true"
}

deny["(COBIT 2019: DSS05.03, ISO 27001:2022: A.8.2) small_container_password must not be a common dictionary password"] {
    common_passwords := {"password", "pswd", "pswd123", "parole"}
    lower(input.variables.small_container_password.value) == common_passwords[_]
}

deny["(COBIT 2019: BAI09.01, ISO 27001:2022: A.5.10) small_container_os must not be Ubuntu"] {
    startswith(lower(input.variables.small_container_os.value), "local:vztmpl/ubuntu")
}

warn["(COBIT 2019: DSS01.04, ISO 27001:2022: A.5.30) small_container_cpu should be minimized"] {
    to_number(input.variables.small_container_cpu.value) > 1
}
package network

import data.network.is_enabled
import data.network.users
import data.network.departments

default accessible = false

# 开关关闭，允许
accessible = true {
    is_enabled = false
}

# 用户绑定的ip符合要求,允许
accessible = true {
    users[input.accessor_id]
    some i
    input.ip >= users[input.accessor_id].nets[i].start_ip
    input.ip <= users[input.accessor_id].nets[i].end_ip
}

# 用户所在部门绑定的ip符合要求，允许
accessible = true {
    users[input.accessor_id]
    dps := users[input.accessor_id].departments
    some i,j
    input.ip >= departments[dps[i]][j].start_ip
    input.ip <= departments[dps[i]][j].end_ip
}

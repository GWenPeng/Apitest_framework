package network

data1 = {
    "is_enabled": false
}

data2 = {
    "is_enabled": true,
    "users": {
        "user03": {
            "nets": [
                {
                    "start_ip": 32,
                    "end_ip": 42
                }
            ]
        },
        "user02": {
            "departments": ["department01", "department02"]
        },
        "user01": {
            "departments": ["department01", "department02"],
            "nets": [
                {
                    "start_ip": 123,
                    "end_ip": 223
                },
                {
                    "start_ip": 3,
                    "end_ip": 4
                }
            ]
        }
    },
    "departments": {
        "department01": [
            {
                "start_ip": 123,
                "end_ip": 323
            },
            {
                "start_ip": 523,
                "end_ip": 623
            }
        ],
        "department02": [
            {
                "start_ip": 123,
                "end_ip": 223
            },
            {
                "start_ip": 55,
                "end_ip": 66
            }
        ]
    }
}

# 开关关闭，使用允许
test_switch_off {
    accessible with input as {"accessor_id": "user01", "ip": 123} with data.network.is_enabled as data1.is_enabled
}

# 用户id不存在
test_user_not_exist {
    accessible == false with input as {"accessor_id": "notexist", "ip": 123} with data.network.users as data2.users
}

# 用户id存在，ip小于最小ip
test_user_not_exist {
    accessible == false with input as {"accessor_id": "user01", "ip": 1} with data.network.users as data2.users
}

# 用户id存在，ip大于最大ip
test_user_not_exist {
    accessible == false with input as {"accessor_id": "user01", "ip": 1111} with data.network.users as data2.users
}

# 用户id存在，ip正确
test_user_not_exist {
    accessible == false with input as {"accessor_id": "user01", "ip": 1111} with data.network.users as data2.users
}

# 用户id存在，ip正确
test_user_not_exist {
    accessible with input as {"accessor_id": "user01", "ip": 3} with data.network.users as data2.users
}

# 用户id存在，ip正确
test_user_not_exist {
    accessible with input as {"accessor_id": "user01", "ip": 4} with data.network.users as data2.users
}

# 用户id存在，ip不符合自身要求，符合所在部门网段的要求
test_user_not_exist {
    accessible with input as {"accessor_id": "user01", "ip": 623} with data.network.users as data2.users with data.network.departments as data2.departments
}

# 用户id存在，ip不符合自身要求，符合所在部门网段的要求
test_user_not_exist {
    accessible with input as {"accessor_id": "user01", "ip": 323} with data.network.users as data2.users with data.network.departments as data2.departments
}
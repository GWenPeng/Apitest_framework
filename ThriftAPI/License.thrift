/*******************************************************************************************
License.thrift
    Copyright (c) Eisoo Software, Inc.(2013 - 2014), All rights reserved

Purpose:
        授权接口.

Author:
    ruan.yulin (ruan.yulin@eisoo.com)

Creating Time:
    2019-04-22
*******************************************************************************************/

include "EThriftException.thrift"

/**
 * 端口
 */
const i32 NCT_LICENSE_PORT = 9602


// 产品授权状态
enum ncTAuthStatus {
    NCT_LS_NOTACTIVE = 1,          // 尚未授权
    NCT_LS_HASACTIVE = 2,           // 已授权
    NCT_LS_HASEXPIRED = 3,          // 已过期
    NCT_LS_HASLAPSED = 4,           // 已失效
}

// 设备授权类型
enum ncTDevAuthType {
    NCT_DAS_NOTAUTH = 1,       // 尚未授权
    NCT_DAS_TEST = 2,          // 测试授权
    NCT_DAS_OFFICIAL = 3,      // 正式授权
}

// 注册码激活状态
enum ncTLicenseStatus {
    NCT_LS_NOTACTIVE = 1,           // 未激活，任何授权码添加后，未激活前的状态
    NCT_LS_HASACTIVE = 2,           // 已激活，任何授权码激活后的状态
    NCT_LS_HASEXPIRED = 3,          // 已过期，测试授权码过期后的状态
    NCT_LS_HASLAPSED = 4,           // 已失效，基本件被删除后，代理件为失效状态
}

// 线上激活结果
enum ncTOnlineActivateResult {
    NCT_AC_SUCCESS = 1,               // 激活成功
    NCT_AC_UPDATE = 2,                // 已激活，更新成功
    NCT_AC_NEWEST = 3,                // 无需变更
}

// 设备信息
struct ncTDeviceInfo {
    1: string softwareType;         // 软件类型 EDMS | ASE | ASC | ASS
    2: string hardwareType;         // 硬件类型
    3: i32 usedNodeNum;             // 已使用节点数
    4: i32 authNodeNum;             // 授权节点数
    5: i64 usedUserNum;             // 已激活用户数
    6: i64 authUserNum;             // 授权用户数
    7: i64 authCapacity;            // 授权容量
    8: ncTAuthStatus authorizedStatus;        // 产品授权状态
    9: i32 expiredDay;              // 多少天过期
    10: i64 endTime;                 // 到期日期
    11: ncTDevAuthType authorizedType; // 设备授权类型
    12: string machineCode;         // 机器码
    13: i64 authExcelUserNum;       // 在线表格授权用户数
}

// 许可证类型
enum ncTlicenseType {
    NCT_NORMAL_TYPE = 0,            // 普通
    NCT_ONLINE_TYPE = 1,            // 在线激活
    NCT_CMP_TYPE = 2,               // CMP
}

// 注册码信息
struct ncTLicenseInfo {
    1: string value;                    // 注册码
    2: string model;                    // 注册码型号
    3: string type;                     // 注册码类型
    4: i32 authNodeNum;                 // 授权节点数
    5: i64 authUserNum;                 // 授权用户数
    6: i64 authCapacity;                // 授权容量
    7: i32 expiredDay;                  // 多少天过期
    8: ncTLicenseStatus status;         // 激活状态（4种值：未激活、已激活、已过期、已失效）
    9: i64 endTime;                     // 到期日期
    10: i64 activeTime;                  // 激活日期
}



// CMP服务器配置
struct ncTCMPHostInfo {
    1: string host;            // CMP服务器地址
    2: i32 port;               // CMP服务器端口
    3: string tenantName;      // 租户账号
    4: string tenantPwd;       // 租户密码
}

enum ncTLicenseError {

    NCT_HARDWARE_AND_LICENSE_NOT_SUITED = 20501,                // 授权码和产品型号不匹配
    NCT_LICENSE_ALREADY_EXISTS = 20502,                         // 授权码已存在
    NCT_LICENSE_HAS_ALREADY_EXPIRED = 20503,                    // 该授权码被使用过，并且已经过期
    NCT_INVALID_LICENSE_TYPE = 20504,                           // 非法的授权码类型
    NCT_CANT_ADD_BASE_LICENSE_CAUSE_ONE_EXISTS = 20505,         // 已存在基本件，不允许添加基本件
    NCT_CANT_ADD_OFFICIAL_LICENSE_CAUSE_TEST_EXISTS = 20506,    // 已存在测试授权码，不允许正式授权码
    NCT_UPGRADE_LICENSE_ALREADY_EXISTS = 20507,                 // 存在相同型号的升级代理，不允许添加升级代理
    NCT_CANT_ADD_TEST_CAUSE_OFFICIAL_LICENSE_EXISTS = 20508,    // 正式授权码存在，不允许添加测试授权码
    NCT_CANT_ADD_TEST_CAUSE_TEST_EXISTS = 20509,                // 测试授权码已存在，不能再添加
    NCT_CANT_ADD_TEST_CAUSE_TEST_USED = 20510,                  // 该设备已经使用过其它测试授权码，不能再添加
    NCT_LICENSE_NOT_EXISTS = 20511,                             // 授权码已不存在
    NCT_LICENSE_ALREADY_ACTIVATED = 20512,                      // 授权码已经被激活过
    NCT_ACTIVE_FAILED_PLEASE_CHECK = 20513,                     // 激活授权码失败，请检查授权码，机器码，激活码是否一致
    NCT_CANT_ACTIVATE_AGENT_LICENSE_CAUSE_BASE_NOT_ACTIVATED = 20514,   // 基本件尚未激活，无法激活代理
    NCT_NOT_ANYSHARE_FAMILY_LICENSE = 20515,                    // 无法添加非AnyShare家族的授权码
    NCT_FAILED_TO_GET_DEVICE_TYPE = 20516,                      // 无法获取产品型号
    NCT_INVALID_LICENSE = 20517,                                // 无效的授权码
    NCT_USER_NUM_OVERFLOW = 20518,                              // 新建/导入的用户数超过授权数
    NCT_PRODUCT_NOT_AUTHORIZED = 20519,                         // 产品尚未授权
    NCT_NODE_NUM_OVERFLOW = 20520,                              // 节点数超过授权数
    NCT_INVALID_NODE_NUM = 20521,                               // 非法的节点数，必须大于等于1
    NCT_EXCEED_MAX_NODE_COUNT = 20522,                          // 无法添加节点代理，已超过产品型号支持的最大节点数
    NCT_EXCEED_MAX_USER_COUNT = 20523,                          // 无法添加用户代理，已超过产品型号支持的最大用户数
    NCT_PRODUCT_HAS_EXPIRED = 20524,                            // 产品授权已过期
    NCT_CANT_DELETE_TIME_AGENT_LICENSE_CAUSE_IT_IS_ACTIVATED = 20525,   // 时长代理已经激活，无法删除
    NCT_CANT_ADD_AGENT_CAUSE_BASE_NOT_EXISTS = 20526,           // 基本件未添加，不允许添加代理
    NCT_NAS_NODE_NUM_OVERFLOW = 20527,                          // NAS服务节点超过节点授权数
    NCT_CONNECT_FAILED = 20528,                                 // 在线激活连接失败
    NCT_INVALID_MACHINE_ID = 20529,                             // 该账号已在其他AnyShare上激活
    NCT_NO_LICENSE = 20530,                                     // 在线激活产品没有授权
    NCT_ANOTHER_ACTIVATE_METHON_USED = 20531,                   // 已经使用了另一种激活方式
    NCT_HARDWARE_NOT_SUPPORT_NAS_OPTION = 20532,                 // 无法激活服务,当前产品型号不支持NAS网关代理授权
    NCT_THE_SAME_OPTION_ALREADY_EXISTS = 20533,                  // 存在相同选件，不允许再次添加
    NCT_EXCEED_MAX_USER_AGENT_COUNT = 20534,                    // 超过最大用户代理数
    NCT_EXCEED_LICENSE_USE_CONDITION = 20535,                   // 超过授权码使用条件


    NCT_CMP_CONNECT_ERROR = 22301,                              // 测试连接失败，指定的服务器连接失败。
    NCT_CMP_AUTH_ERROR = 22302,                                 // 测试连接失败，指定的服务器无法访问。
    NCT_CMP_INVALID_IP_OR_HOST = 22303,                         // 非法的ip或者域名
    NCT_CMP_INVALID_PORT = 22304,                               // 非法的端口

    NCT_CMP_INVALID_TENANT_NAME = 22309,                        // 租户账户不合法
    NCT_CMP_INVALID_TENANT_PWD = 22310,                         // 租户密码不合法
    NCT_CMP_USER_OR_PASSWD_ERROR = 22311,                       // 租户账户或密码错误
    NCT_CMP_NODE_ALREADY_ADDED = 22312,                         // 平台已有该节点
    NCT_CMP_NODE_ALREADY_AUTHORIZED = 22313,                    // 该节点已授权
    NCT_CMP_RESPONSE_TIMEOUT = 22314,                           // cmp响应超时
    NCT_CMP_NODE_ALREADY_REGISTERED = 22315,                    // 该节点已被其他的用户接入过
    NCT_CMP_GET_LICENSE_FAILED = 22316,                         // 手动获取CMP授权失败

}

/**
 * License 管理服务接口
 */
service ncTLicense {

    // ----------------------------------------------------------------------------
    // 一 授权管理
    // ----------------------------------------------------------------------------
    // 1.1 获取设备信息，包括设备型号，激活状态，授权信息
    ncTDeviceInfo Licensem_GetDeviceInfo() throws(1: EThriftException.ncTException exp)

    // 1.2 添加单个授权码
    ncTLicenseInfo Licensem_AddLicense(1: string license) throws(1: EThriftException.ncTException exp)

    // 1.3 删除授权码
    void Licensem_DeleteLicense(1: string license) throws(1: EThriftException.ncTException exp)

    // 1.4 激活授权码
    void Licensem_ActivateLicense(1: string license, 2: string activeCode)
                                    throws(1: EThriftException.ncTException exp)

    // 1.5 获取已添加的授权码
    list<ncTLicenseInfo> Licensem_GetAllLicenses() throws(1: EThriftException.ncTException exp)

    // 1.6 检查nodeNum是否超过授权数
    // 如果节点授权为2，nodeNum小于或者等于2，正常返回
    // 如果节点授权为2，nodeNum为3，抛出异常，错误码为：NCT_NODE_NUM_OVERFLOW
    void Licensem_CheckNodeNumOverflow(1: i32 nodeNum) throws(1: EThriftException.ncTException exp)

    // 1.7 自动授权产品
    void Licensem_AutoAuthorized(1: string password) throws(1: EThriftException.ncTException exp)

    // 1.8 检查nodeNum是否超过NAS授权数
    void Licensem_CheckNasNumOverflow(1: i32 nodeNum) throws(1: EThriftException.ncTException exp)

    // 1.9 线上激活
    ncTOnlineActivateResult Licensem_OnlineActivate(1: string url, 2: string account, 3: string password)
                                                    throws(1: EThriftException.ncTException exp)

    // 1.10 获取AnyRobot安全文件分析选件状态：true--开启， false--关闭
    bool Licensem_GetAnyRobotOptionStatus() throws(1: EThriftException.ncTException exp)

    // 1.11 获取机器码
    string Licensem_GetMachineCode() throws(1: EThriftException.ncTException exp)

    // 1.12 获取授权信息，包括基本件或测试授权信息，授权数，节点数，签名等
    string Licensem_GetAuthInfo() throws(1: EThriftException.ncTException exp)

    // 1.13 根据站点ID获取站点用户信息，包括已启用用户数，签名等
    string Licensem_GetSiteUserInfo (1: string siteId) throws (1: EThriftException.ncTException exp)

    // 1.14 获取站点授权用户数
    i32 Licensem_GetSiteUserAuthNum (1: string siteId) throws (1: EThriftException.ncTException exp)

    // 1.15 获取站点授权状态
    i32 Licensem_GetSiteAuthStatus (1: string siteId) throws (1: EThriftException.ncTException exp)

    // 1.16 获取nas节点授权数
    i32 Licensem_GetNASAuthNodeNum () throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 二、CMP接入管理
    // ----------------------------------------------------------------------------
    // 2.1 获取CMP服务器信息
    ncTCMPHostInfo CMP_GetHostInfo() throws (1: EThriftException.ncTException exp);

    // 2.2 设置CMP服务器信息
    void CMP_SetHostInfo(1: ncTCMPHostInfo cmpHostInfo) throws (1: EThriftException.ncTException exp);

    // 2.3 测试CMP服务器连接
    void CMP_Test(1: ncTCMPHostInfo cmpHostInfo) throws (1: EThriftException.ncTException exp);

    // 2.4 模拟CMP授权下发消息，返回cmp约定的消息回复内容
    string CMP_SimulateLicenseMessage(1: string msg) throws (1: EThriftException.ncTException exp);

    // 2.5 手动从CMP获取授权
    void CMP_GetLicenseInfo() throws(1: EThriftException.ncTException exp);
}
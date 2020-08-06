/***************************************************************************************************
EACP.thrift:
    Copyright (c) Eisoo Software, Inc.(2009 - 2013), All rights reserved

Purpose:
    定义了 EACP 对外开放的 thrift 服务接口

Author:
    zou.yongbo@eisoo.com

Creating Time:
    2013-07-29
***************************************************************************************************/
include "EThriftException.thrift"

// 服务端口号
const i32 NC_T_EACP_PORT = 9992;

struct ncTCustomPerm {
    1: string           accessorId;         // 访问者id
    2: i16              accessorType;       // 访问者类型
    3: bool             isAllowed;          // 允许/拒绝
    4: i32              permValue;          // 权限值
    5: i64              endTime;            // 截止时间
}

// ncTLoginDeviceBaseInfo
struct ncTLoginDeviceBaseInfo {
    1: string       udid;             // 设备唯一标识号
    2: string       name;             // 设备名称
    3: i32          osType;           // 操作系统类型
    4: string       deviceType;       // 设备类型
    5: string       lastLoginIp;      // 上次登录ip
    6: i64          lastLoginTime;    // 上次登录时间
}

// ncTLoginDeviceInfo
struct ncTLoginDeviceInfo {
    1: ncTLoginDeviceBaseInfo    baseInfo;       // 基础信息
    2: i32                       eraseFlag;      // 缓存擦除标识
    3: i64                       lastEraseTime;  // 上次缓存擦除时间
    4: i32                       disableFlag;    // 禁用标识
    5: i32                       bindFlag;       // 标定标识
    6: i32                       loginFlag;   // 是否登录标识
}

// 内外网数据交换流程信息
struct ncTDocExchangeProcessInfo {
    1:string                     userId;            // 发起人
    2:string                     docId;             // 文档id
    3:string                     applyMsg;          // 申请信息
    4:string                     dstDocName;        // 接收人、目的目录
    5:string                     dstDir;            // 目的目录
    6:bool                       toInbox;           // dstDir是否在接收文件箱下
    7:bool                       isLibSync;         // 是否为文档库同步发起的交换流程
}

// 文件自动锁配置
struct ncTAutolockConfig {
    1: bool                      isEnable;          // 是否开启
    2: i64                       expiredInterval;   // 过期时间时间间隔
}

// eacp错误码
enum ncTEACPError {
    NCT_DB_OPERATE_FAILED = 10001,                              // 数据库执行失败
    NCT_UNKNOWN_ERROR = 10002,                                  // 未知错误

    NCT_INVALID_URL = 20001,                                    // Url参数错误
    NCT_INVALID_JSON = 20002,                                   // 非法Json

    NCT_LOGIN_DEVICE_EXISTS = 20101,                            // 无法添加设备，该登录设备已经存在

    NCT_INVALID_LIMIT_VALUE = 20210,                            // limit参数错误，不应小于-1。

    NCT_MAC_ADDR_INVALID = 20217,                               // MAC地址不合法

    NCT_INVALID_EXPIRED_INTERVAL = 20401,                       // 文件锁超时时间不合法

}

// check token info
struct ncTCheckTokenInfo {
    1:string                userId;            // 用户id
    2:string                tokenId;           // token id
    3:string                ip;                // 登录设备ip
}

// 杀毒操作类型
enum ncTAntivirusOperationType {
    NCT_ISOLATION = 1,      // 病毒文件被隔离
    NCT_REPAIR = 2,         // 病毒文件被修复
}

// 杀毒消息
struct ncTAntivirusMessage {
    1: string receiverId;                           // 消息发送者ID
    2: string senderId;                             // 消息接收者ID
    3: string antivirusAdmin;                       // 防病毒管理员
    4: string docId;                                // 文件GNS路径
    5: string url;                                  // 文件内链接路径
    6: ncTAntivirusOperationType antivirusOp;       // 病毒文件操作类型 隔离，修复，还原
    7: i32 accessorType;                            // 访问者类型 1 为 user， 2 为 department， 3 为 contactor
    8: bool isDir;                                  // 是否是目录
}

// 隔离消息类型
enum ncTQuarantineMSGType {
    NCT_QUARANTINE = 1,      // 隔离
    NCT_RESTORE = 2,         // 还原
    NCT_APPROVE = 3,         // 申诉被通过
    NCT_VETO = 4,            // 申诉被否决
}

// 隔离消息
struct ncTQuarantineMessage {
    1: string senderId;                             // 消息发送者ID
    2: string docId;                                // 文件GNS路径
    3: string url;                                  // 文件内链接路径
    4: ncTQuarantineMSGType msgType;                // 隔离消息类型 隔离，还原
    5: string creatorId;                            // 文件创建者
    6: string modifierId;                           // 文件最新修改者
    7: i32 csflevel;                                // 文件密级
    8: i32 quarantineType;                          // 隔离类型 1：非法 2：染毒 3：涉黄
    9: i32 processType;                             // 隔离文件处理类型 0: 隔离 1: 修复 (只用于染毒文件隔离)
}

// 申诉消息
struct ncTAppealMessage {
    1: string senderId;                             // 消息发送者ID
    2: string docId;                                // 文件GNS路径
    3: string url;                                  // 文件内链接路径
    4: ncTQuarantineMSGType msgType;                // 隔离消息类型 隔离，还原
    5: string creatorId;                            // 文件创建者
    6: string modifierId;                           // 文件最新修改者
    7: i32 csflevel;
    8: string appealSuggest;                        // 申诉的处理意见
}

// 文件到期通知消息
struct ncTDocRemindMessage {
    1: string docId;                                // 文件GNS路径
    2: bool isDir;                                  // 是否是目录
    3: string url;                                  // 文件内链接路径
    4: i32 csflevel;                                // 文件密级
    5: i64 dueDate;                                 // 文件到期时间
    6: list<string> receivers;                      // 被通知人
    7: string remindContent;                        // 通知消息内容
}

// EACP Thrift Service
service ncTEACP {
    /**
     * 获取eacp的用户在线数
     *
     * @ret: 返回在线用户数
     * @throw EThriftException.ncTException
     */
    i32 EACP_GetOnlineUserCount ()
        throws (1: EThriftException.ncTException exp);

    /**
     * 获取eacp的用户租户在线数
     *
     * @ret: 返回在线用户数
     * @throw EThriftException.ncTException
     */
    i32 EACP_GetTenantOnlineUserCount (1: string orgId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 删除用户时，删除用户文档，该用户对应的权限配置，该用户的token信息，所有者信息
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EACP_OnDeleteUser (1: string userId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 删除用户组时
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EACP_OnDeleteGroup (1: string groupId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 删除部门时通知eacp删除权限
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EACP_OnDeleteDepartment (1: list<string> departmentIds)
        throws (1: EThriftException.ncTException exp);

    /**
     * 清除超出共享范围的权限配置
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EACP_ClearPermOutOfScope ( )
        throws (1: EThriftException.ncTException exp);

    /**
     * 清除未开启外链共享用户或部门的外链共享信息
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EACP_ClearLinkOutOfScope ( )
        throws (1: EThriftException.ncTException exp);

    /**
     * 清除未开启发现共享用户或部门的发现共享信息
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EACP_ClearFindOutOfScope ( )
        throws (1: EThriftException.ncTException exp);

    /**
     * 获取注册码模块信息
     *
     * @param license:          注册码
     * @return:                 注册码对应的模块信息
     */
    string EACP_GetLicenseInfo (1: string license)
        throws (1: EThriftException.ncTException exp);

    /**
     * 验证离线激活码是否正确
     *
     * @param license:          注册码
     * @param machineCode:      机器码
     * @param activeCode:       激活码
     * @return:                 激活结果,0:成功
     */
    i32 EACP_VerifyActiveCode (1: string license, 2: string machineCode, 3: string activeCode)
        throws (1: EThriftException.ncTException exp);

    /**
     * 获取自动锁配置
     */
    ncTAutolockConfig EACP_GetAutolockConfig () throws (1: EThriftException.ncTException exp);

    /**
     * 设置自动锁配置
     */
    void EACP_SetAutolockConfig (1: ncTAutolockConfig config) throws (1: EThriftException.ncTException exp);

    /**
     * 获取用户的设备信息
     * @param userId:           用户id
     * @paeam start:            起始索引
     * @param limit             获取设备信息条数
     * @ret:                    用户的登录设备信息
     * @throw EThriftException.ncTException
     */
    list<ncTLoginDeviceInfo> EACP_GetDevicesByUserId(1: string userId, 2: i32 start, 3: i32 limit) throws (1: EThriftException.ncTException exp);

    /**
     * 添加设备信息
     * @param userId:           用户id
     * @param udid:             设备唯一标识码
     * @param osType:           设备类型 0：Unknown, 1：IOS, 2：Android, 4：Windows, 5：MacOSX
     * @ret:                    无返回
     * @throw EThriftException.ncTException
     */
    void EACP_AddDevice(1: string userId, 2: string udid, 3: i32 osType) throws (1: EThriftException.ncTException exp);

    /**
     * 添加设备信息
     * @param userId            用户id
     * @param udids:            设备唯一标识码
     * @param osType            操作系统类型 0：Unknown, 1：IOS, 2：Android, 4：Windows, 5：MacOSX
     * @ret:                    添加失败的设备mac地址
     * @throw EThriftException.ncTException
     */
    list<string> EACP_AddDevices(1: string userId, 2: list<string> udids, 3: i32 osType) throws (1: EThriftException.ncTException exp)

    /**
     * 获取用户的指定设备信息
     * @param userId:           用户id
     * @param udid:             设备唯一标识号
     * @param start:            起始索引
     * @param limit             获取设备信息条数
     * @param ret:              用户的指定设备信息
     * @throw EThriftException.ncTException
     */
    list<ncTLoginDeviceInfo> EACP_SearchDevicesByUserIdAndUdid(1: string userId, 2: string udid, 3: i32 start, 4: i32 limit) throws (1: EThriftException.ncTException exp);

    /**
     * 通过部分udid字符获取可能的设备标识号
     * @param key:              设备识别号关键字
     * @param start:            起始索引
     * @param limit             获取设备信息条数
     * @param ret:              设备唯一标识号
     * @throw EThriftException.ncTException
     */
    list<string> EACP_SearchDevices(1: string key, 2: i32 start, 3: i32 limit) throws (1: EThriftException.ncTException exp);

    /**
     * 获取绑定了此设备的用户
     * @param udid:             设备唯一标识号
     * @param start:            起始索引
     * @param limit             获取设备信息条数
     * @ret:                    用户名列表
     * @throw EThriftException.ncTException
     */
    list<string> EACP_SearchUserByDeviceUdid(1: string udid, 2: i32 start, 3: i32 limit) throws (1: EThriftException.ncTException exp);

    /**
     * 删除设备信息
     * @param userId:           用户id
     * @param udids:            设备唯一标识码；如果为空，删除用户的所有设备
     * @ret:                    无返回
     * @throw EThriftException.ncTException
     */
    void EACP_DeleteDevices(1: string userId, 2: list<string> udids) throws (1: EThriftException.ncTException exp);

    /**
     * 绑定设备
     * @param userId:           用户id
     * @param udid:             设备唯一标识码
     * @ret:                    无返回
     * @throw EThriftException.ncTException
     */
    void EACP_BindDevice(1: string userId, 2: string udid) throws (1: EThriftException.ncTException exp);

    /**
     * 解绑设备
     * @param userId:           用户id
     * @param udid:             设备唯一标识码
     * @ret:                    无返回
     * @throw EThriftException.ncTException
     */
    void EACP_UnbindDevice(1: string userId, 2: string udid) throws (1: EThriftException.ncTException exp);

    /**
     * 启用设备
     * @param userId:           用户id
     * @param udid:             设备唯一标识码
     * @ret:                    无返回
     * @throw EThriftException.ncTException
     */
    void EACP_EnableDevice(1: string userId, 2: string udid) throws (1: EThriftException.ncTException exp);

    /**
     * 禁用设备
     * @param userId:           用户id
     * @param udid:             设备唯一标识码
     * @ret:                    无返回
     * @throw EThriftException.ncTException
     */
    void EACP_DisableDevice(1: string userId, 2: string udid) throws (1: EThriftException.ncTException exp);

    /**
     * 配置GNS路径的权限信息，注意不要包含继承的权限
     * 会自动分析差异，然后进行权限配置
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_SetPermConfigs(1: string docId, 2: list<ncTCustomPerm> permConfigs) throws (1: EThriftException.ncTException exp);

    /**
     * 清空用户当前的所有token信息
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_ClearTokenByUserId(1: string userId) throws (1: EThriftException.ncTException exp);

    /**
     * 流程变更时，通知eacp删除对应的申请记录
     * @ret:
     * @throw EThriftException.ncTException
     */
     void EACP_OnProcessChange(1: string processId) throws (1: EThriftException.ncTException exp);

    /**
     * 清空所有用户token信息
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_ClearAllToken() throws (1: EThriftException.ncTException exp);

    /**
     * 管理员禁止指定设备登录时, 更新所有token flag信息
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_UpdateAllTokenFlagByOsType(1:i32 osType) throws (1: EThriftException.ncTException exp);

    /**
     * 管理员禁止身份证号登录时, 更新相关token flag信息
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_UpdateAllTokenFlagByIdcardStatus() throws (1: EThriftException.ncTException exp);

    /**
     * 检查用户tokenid接口
     * @ret:
     * @throw EThriftException.ncTException
     */
    bool EACP_CheckTokenId(1:ncTCheckTokenInfo tokenInfo) throws (1: EThriftException.ncTException exp);

    /**
     * 清空所有用户共享邀请链接
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_ClearAllInvitationInfo() throws (1: EThriftException.ncTException exp);

    /**
     * 清空冻结用户共享邀请链接
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_ClearUserInvitationInfo(1:string userId) throws (1: EThriftException.ncTException exp);

    /**
     * 重启所有节点 sharemgnt_server 服务
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_RestartGlobalShareMgntServer() throws (1: EThriftException.ncTException exp);

    /**
     * 重启当前节点 sharemgnt_server 服务
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_RestartLocalShareMgntServer() throws (1: EThriftException.ncTException exp);

    /**
     * 设置消息推送到的第三方Id
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_SetPushMessagesConfig(1:string appId) throws (1: EThriftException.ncTException exp);

    /**
     * 获取消息推送到的第三方Id
     * @ret:
     * @throw EThriftException.ncTException
     */
    string EACP_GetPushMessagesConfig() throws (1: EThriftException.ncTException exp);

    /**
     * 发起内外网数据交换流程
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_PublishDocExchange(1:ncTDocExchangeProcessInfo params) throws (1: EThriftException.ncTException exp);

    /**
     * 添加杀毒消息
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_AddAntivirusMessage(1:ncTAntivirusMessage msg) throws (1: EThriftException.ncTException exp);

    /**
     * 添加隔离消息
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_AddQuarantineMessage(1:ncTQuarantineMessage msg) throws (1: EThriftException.ncTException exp);

    /**
     * 添加申诉处理消息
     * @ret:
     * @throw EThriftException.ncTException
     */
     void EACP_AddAppealMessage(1:ncTAppealMessage msg) throws (1: EThriftException.ncTException exp);

    /**
     * 添加文件到期通知消息
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_AddDocRemindMessage(1:ncTDocRemindMessage msg) throws (1: EThriftException.ncTException exp);

    /**
     * 设置邮件通知分享开关状态
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_SetSendShareMailStatus(1:bool status) throws (1: EThriftException.ncTException exp);

    /**
     * 获取邮件通知分享开关状态
     * @ret:
     * @throw EThriftException.ncTException
     */
    bool EACP_GetSendShareMailStatus() throws (1: EThriftException.ncTException exp);

    /**
     * 更新禁用用户token flag信息
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_UpdateTokenFlagByUserId(1:string userId, 2:i32 flag) throws (1: EThriftException.ncTException exp);

    /**
     * 根据权重值更新用户token flag信息
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_UpdateTokenFlagByPriority(1:i32 priority, 2:i32 flag) throws (1: EThriftException.ncTException exp);

    /**
     * 设置消息通知状态
     * @ret:
     * @throw EThriftException.ncTException
     */
     void EACP_SetMessageNotifyStatus(1:bool status) throws (1: EThriftException.ncTException exp);

    /**
     * 获取消息通知状态
     * @ret:
     * @throw EThriftException.ncTException
     */
     bool EACP_GetMessageNotifyStatus() throws (1: EThriftException.ncTException exp);

    /**
     * 删除用户时清除该用户给联系人组配置的权限
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_DeleteContactPermByUserID(1:string dbName, 2:string userId) throws (1: EThriftException.ncTException exp);

    /**
     * 设置定制化的应用配置
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_SetCustomApplicationConfig (1: string appConfig) throws (1: EThriftException.ncTException exp);

    /**
     * 获取定制化的应用配置
     * @ret:
     * @throw EThriftException.ncTException
     */
    string EACP_GetCustomApplicationConfig () throws (1: EThriftException.ncTException exp);

    /**
     * 通知线程发送 webhook 通知
     *
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EACP_NotifyPushWebhookThread() throws (1: EThriftException.ncTException exp);
}

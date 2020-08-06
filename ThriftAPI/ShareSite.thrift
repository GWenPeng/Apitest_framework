/********************************************************************************
ShareSite.thrift:
    分布式站点管理功能的thrift接口定义文件
    Copyright (c) Eisoo Software, Inc.(2004 - 2013), All rights reserved.

Purpose:
    此接口文件定义AnyShare分布式部署站点管理接口

Author:
    wei.xiaodong@eisoo.com

Creating Time:
    2016-02-29

简介：
ShareSite提供AnyShare站点管理的Thrift接口，包括:
1. 多站点模式设置
2. 添加站点
3. 删除站点
4. 编辑站点
5. 获取站点信息
6. 获取站点类型
7. 搜索站点

二、ShareSite提供的错误码说明：
ShareSite提供的错误码共5位，如10111。第一位表示错误级别，二三位表示模块类型，四五位表示具体错误信息。
模块状态码信息如下：
*********************************************************************************/

include "EThriftException.thrift"
const i32 NCT_SHARESITE_PORT = 9601

// 站点类型
enum ncTSiteType {
    NCT_SITE_TYPE_NORMAL = 0,        // 普通站点类型
    NCT_SITE_TYPE_MASTER = 1,        // 主站点类型
    NCT_SITE_TYPE_SLAVE = 2,         // 从站点类型
}

// 站点病毒库更新状态
enum ncTSiteVirusStatus{
    NCT_COMPLETE_UPDATE = 0;    // 病毒库更新完成
    NCT_NEED_UPDATE = 1,        // 请求更新病毒库
}

// 站点信息
struct ncTSiteInfo{
    1: string id;               //站点ID
    2: string ip;               //站点访问地址
    3: string name;             //站点名称
    4: ncTSiteType type;        //站点类型
    5: i16 linkStatus;          //站点连接状态(0: 离线， 1:在线)
    6: i64 usedSpace;           //站点已使用存储空间
    7: i64 totalSpace;          //站点总存储空间
    8: string siteKey;          //站点秘钥
    9: string masterIp;         //主站点访问地址（用于分站点更新时通知主站点更新）
    10: i16 isSync;             //是否同步
    11: i16 siteStatus;         //站点状态(0: 禁用， 1:启用)
    12: i64 heartRate;          //站点心率值(0: 禁用， 1:启用)
    13: string masterDbIp;      //主站点数据库ip
    14: bool siteVirusDBStatus; //站点的病毒库状态
}

//添加站点相关参数
struct ncTAddSiteParam{
    1: string ip;               //站点访问地址
    2: string name;             //站点名称
    3: string siteKey;          //站点秘钥
}

//编辑站点相关参数
struct ncTEditSiteParam{
    1: string id;               //站点ID
    2: string ip;               //站点访问地址
    3: string name;             //站点名称
}

// 错误码
enum ncTShareSiteError {
    NCT_SITE_NETWORK_NOT_AVAILABLE = 10001,         //分站点访问地址不可用
    NCT_SITE_NOT_ENABLE_MULTIMODE = 10002,          //站点未开启多站点模式
    NCT_SITE_NAME_IS_OCCUPT = 10003,                //该站点名被占用
    NCT_SITE_UNKNOWN_ERROR = 10004,                 //分站点内部执行错误
    NCT_SITE_HAS_BEEN_ADDED = 10005,                //站点已被添加
    NCT_SITE_NAME_NOT_VALID = 10006,                //站点名输入不合法
    NCT_SITE_NOT_HAS_BEEN_ADDED = 10007,            //站点未被添加
    NCT_SITE_HAS_OFF_LINE = 10008,                  //站点已离线
    NCT_SITE_HAS_BEEN_MASTER = 10009,               //站点已成为其他分站点的总站点
    NCT_SITE_NOT_MASTER_CATNOT_ADD_SITE = 10010,    //当前站点不是总站点，无法添加其他站点
    NCT_SITE_SLAVE_CANNOT_SET_MULTIMODE = 10011,    //当前站点为分站点,不能设置多站点模式
    NCT_SITE_CANNOT_DELETE_LOCAL_SITE = 10012,      //不能移除本站点
    NCT_SITE_PARAM_ERROR = 10013,                   //参数错误
    NCT_SITE_KEY_ERROR = 10014,                     //秘钥不匹配
    NCT_SITE_ID_NOT_EXIST = 10015,                  //站点id不存在
    NCT_SITE_REQUEST_EXPIRED = 10016,               //请求已过期
    NCT_SITE_CANNOT_ADD_LOCAL_SITE = 10017,         //不能添加本站点
    NCT_MASTER_SITE_CAN_NOT_MODIFY_IP = 10018,      //主站点不能修改自己的ip
    NCT_SITE_ALREADY_EXISTS = 10019,                //分站点已存在，不能重复添加。
    NCT_SITE_NOT_AUTHORIZED = 10020,                //分站点未授权。不能添加
    NCT_DEVICE_CANNOT_BE_MASTER_SITE = 10021,       //该产品型号不能作为总站点
}

service ncTShareSite {
    // ----------------------------------------------------------------------------
    // 站点管理
    // ----------------------------------------------------------------------------

    // 设置多站点状态(开启或关闭) (true: 开启， false: 关闭)
    void SetMultSiteStatus(1:bool status) throws (1:EThriftException.ncTException exp);

    // 获取多站点状态(开启或关闭) (true: 开启， false: 关闭)
    bool GetMultSiteStatus() throws (1:EThriftException.ncTException exp);

    //获取本地站点信息
    ncTSiteInfo GetLocalSiteInfo() throws (1:EThriftException.ncTException exp);

    // 增加分站点
    void AddSite(1:ncTAddSiteParam paramInfo) throws (1:EThriftException.ncTException exp);

    // 删除分站点
    void DeleteSite(1:string siteID) throws (1:EThriftException.ncTException exp);

    // 编辑站点信息
    void EditSite(1: ncTEditSiteParam paramInfo) throws (1:EThriftException.ncTException exp);

    // 获取站点信息
    list <ncTSiteInfo> GetSiteInfo() throws (1:EThriftException.ncTException exp);

    // 通知站点开始添加, 主要完成分站点是否可被添加及返回分站点信息
    ncTSiteInfo NodifySiteAddBegin() throws (1:EThriftException.ncTException exp);

    // 通知站点添加
    void NodifySiteAdd(1:string masterIp) throws (1:EThriftException.ncTException exp);

    // 通知站点移除
    void NodifySiteDelete() throws (1:EThriftException.ncTException exp);

    //获取本地站点信息
    ncTSiteInfo GetLocalSiteInfoByRemote() throws (1:EThriftException.ncTException exp);

    //更新分站点心率值
    void UpdateHeartByMaster(1:string siteId) throws (1:EThriftException.ncTException exp);

    //向主站点同步更新分站点数据
    void SyncSlaveToMaster(1:string data) throws (1:EThriftException.ncTException exp);

    //向分站点同步更新主站点数据
    void SyncMasterToSlave(1:string data) throws (1:EThriftException.ncTException exp);

    //更新站点信息中的host
    void UpdateSiteIp(1:string ip) throws (1:EThriftException.ncTException exp);

    //通过站点id获取站点信息
    ncTSiteInfo GetSiteInfoById(1:string siteid) throws (1:EThriftException.ncTException exp);

    //验证签名
    void CheckSign(1:string expired, 2:string sign, 3:string site_id, 4:bool flag) throws (1:EThriftException.ncTException exp);

    //重启服务
    void RestartServer(1:string server_name) throws (1:EThriftException.ncTException exp);

    // 更新EVFS中的站点信息
    void UpdateEVFSSiteInfo() throws (1:EThriftException.ncTException exp);

    // 创建跨域文件
    void CreateCrossDomainXml() throws (1:EThriftException.ncTException exp);

    //更新站点信息中的主站点数据库ip
    void UpdateSiteMasterDbIp(1:string ip) throws (1:EThriftException.ncTException exp);

    //同步对象存储信息
    void SyncOSSInfo(1:string data) throws (1:EThriftException.ncTException exp);

    // 分站点调用，用于更新当前分站点的病毒库状态
    void UpdateSiteVirusStatus(1: bool Status) throws (1: EThriftException.ncTException exp)

    // 主站点调用，用于更新所有分站点的病毒库状态
    void UpdateAllSiteVirusStatus(1: bool Status) throws (1: EThriftException.ncTException exp)

    // 分站点调用，用于获取当前分站点的病毒库状态
    bool GetSiteVirusStatus() throws (1: EThriftException.ncTException exp)
}

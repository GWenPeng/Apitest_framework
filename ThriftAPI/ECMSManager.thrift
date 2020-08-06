/*********************************************************************
ECMSManager.thrift:
    爱数集群配置管理接口定义文件

Purpose:
    提供集群业务逻辑层对外接口。
    thrift生成的remote客户端工具，访问示例如下：
    python ncTECMSManager-remote -h host:port interface param

    eg:
        python ncTECMSManager-remote -h 192.168.100.100:9201 get_all_node_info

Author:
    zhang.tao@eisoo.com
    tong.sha@eisoo.com
    wu.yuzhe@eisoo.com
    huang.sihan@eisoo.com
    chen.liang@eisoo.com

Creating Time:
    2017-08-10

ECMSManager提供集群管理的Thrift接口，包括:
1、集群部署
2、数据库管理
3、防火墙管理
4、高可用管理
5、节点管理
6、存储管理
7、监控告警管理
8、节点角色管理
9、应用服务管理
10、登陆管理
11、分布式配置管理
12、外部时间源管理
13、服务模块化管理

**********************************************************************/

include "EThriftException.thrift"
include "ECMSAgent.thrift"


// 端口号
const i32 NCT_ECMSMANAGER_PORT = 9201

// 部署模式
const string NCT_STANDARD_MODE = 'standard'
const string NCT_PROFESSIONAL_MODE = 'professional'
const string NCT_CLOUD_MODE = 'cloud'

/**
 * 集群基本信息
 */
struct ncTClusterInfo {
    1: string cluster_uuid = '',     // 集群 uuid
}

/**
 * 数据库节点结构
 */
struct ncTDBNodeInfo{
    1: string node_uuid,             // 节点uuid
    2: string node_alias = '',       // 节点别名
    3: string node_ip,               // 节点ip
    4: string db_role,               // 数据库角色 master:主数据库 | slave:从数据库
    5: string service_status,        // 数据库端口服务状态: "running", "stopped", "errorxxx"
    6: string slave_status,          // 数据库端口同步状态: "running", "stopped", "", "errorxxx"
                                     //                     单节点场景下为 ""
                                     //                     查询出错的情况下为具体错误"errorxxx"
    7: bool is_online,               // 节点在线状态
}

/**
 * 应用节点结构
 */
struct ncTAppNodeInfo{
    1: string node_uuid,              // 节点uuid
    2: string node_alias,             // 节点别名
    3: string node_ip,                // 节点ip
    4: bool service_status,           // 应用服务状态
    5: bool lvs_status,               // 节点lvs状态
    6: bool is_online,                // 节点在线状态
}

/**
 * 存储节点结构
 */
struct ncTStorageNodeInfo{
    1: string node_uuid,              // 节点uuid
    2: string node_alias,             // 节点别名
    3: string node_ip,                // 节点ip
    4: bool service_status,           // 存储服务状态
    5: bool lvs_status,               // 节点lvs状态
    6: bool is_online,                // 节点在线状态
}

// 应用服务结构
struct ncTAppServiceInfo {
    1: string   name,                   // 服务名
    2: i32      port,                   // 服务所监听的端口, 0 为不监听端口
    3: bool     is_lvs,                 // 是否被 lvs 转发
}

// 高可用节点所属子系统
enum ncTHaSys{
    NORMAL = 0                          // 非ha节点
    BASIC = 1,                          // 集群使用全局高可用，vip和ivip在同一节点情况
    APP = 2,                            // 应用子系统vip
    STORAGE = 3,                        // 存储子系统vip
    DB = 4,                             // 数据库使用的ivip标识
}

/**
 * vip信息
 */
struct ncTVipInfo {
    1: string vip = '',                   // ip地址
    2: string mask = '',                  // 掩码
    3: string nic = '',                   // 使用网卡
    4: i32 sys = ncTHaSys.BASIC,          // vip所属子系统(与高可用节点结构的sys对应)
}

/**
 * 高可用节点结构
 */
struct ncTHaNodeInfo {
    1: string node_uuid = '',             // 节点uuid
    2: string node_alias = '',            // 节点别名
    3: string node_ip = '',               // 节点ip
    4: bool is_online = true,             // 节点在线状态
    5: bool is_master = false,            // 节点是否是ha主节点
    6: i32 sys = ncTHaSys.BASIC,          // vip所属子系统
}

/**
 * 节点信息结构
 */
struct ncTNodeInfo {
    1: string node_uuid = '',             // 节点uuid
    2: i32 role_db = 0,                   // 数据库节点标识(0:非数据库节点
                                          //                1:数据库master节点
                                          //                2:数据库slave节点)
    3: i32 role_ecms = 0,                 // 集群管理节点标识(0:非集群管理节点；1:集群管理主节点)
    4: i32 role_app = 0,                  // 应用节点标识   0:非应用节点；1:应用节点
    5: i32 role_storage = 0,              // 存储节点标识   0:非存储节点；1:存储节点
    6: string node_alias = '',            // 节点别名
    7: string node_ip = '',               // 节点加入集群使用的IP
    8: bool is_online = true,             // 节点在线状态(true:在线 | false离线)
    9: i32 is_ha = 0,                     // 节点是否是ha节点
    10: i32 is_etcd = 0,                  // 节点是否有etcd实例(0: 没有实例
                                          //                    1: 只有有一个实例
                                          //                    2: 有两个实例(ecms节点的备实例存在)
    11: bool consistency_status = true,   // 节点一致性状态(true: 与集群状态一致 | false: 不一致)
}

/**
 * 防火墙信息结构
 */
struct ncTFirewallInfo {
    1: i32 port = 0,                      // 端口号
    2: string protocol = 'tcp',           // 协议类型 (tcp or udp)
    3: string source_net = '',            // 源网络地址 (ip/netmask e.g:192.168.4.1/255.255.255.0)
    4: string dest_net = '',              // 目的网络地址 (ip/netmask e.g:192.168.4.1/255.255.255.0)
    5: string role_sys = '',              // 'ecms'    集群管理节点规则标识
                                          // 'app'     应用节点规则标识
                                          // 'db'      数据库节点规则标识
                                          // 'storage' 存储节点规则标识
                                          // 'basic'   公共规则标识
    6: string service_desc = '',          // 放行端口对应的服务描述信息
}

/**
 * 存储池设备信息
 */
struct ncTStoragePoolDevice {
    // swift 虚拟设备信息
    1: required ECMSAgent.ncTSwiftDevice swift_device,
    // 数据卷信息
    // 当 data_volume 为 None 或 data_volume.mount_path 为空 时，则该设备在存储池中意味着已离线
    2: optional ECMSAgent.ncTDataVolume data_volume,
}

/**
 * 存储池信息
 */
struct ncTStoragePool {
    // swift ring 信息
    1: required ECMSAgent.ncTSwiftRing ring,
    // 存储池的逻辑已用空间
    2: optional double logical_used_size_gb,
    // 存储池的物理已用空间
    3: optional double physical_used_size_gb,
}

/**
 * 本地 Ceph 存储信息
 */
struct ncTCephStorageInfo {
    // 已用空间
    1: optional double used_size_gb,
    // 总容量
    2: optional double capacity_gb,
}

// 配置文件信息
struct ncTConfFileInfo {
    1: string conf_file_path,             // 配置文件路径
    2: string conf_file_md5,              // 配置文件md5
    3: string modified_time,
}

// 监控系统异常记录
struct ncTMonitorProblemRecord {
    1: i64 objectid,            // 触发异常的 triggerid, 或历史数据异常的 itemid
    2: string description,      // trigger 或 item 的名称
    3: i64 timestamp,           // 异常发生的时间
    4: i64 timestamp_recovery,  // 异常恢复正常的时间
    5: bool value,              // 异常是否处于异常, False: 已恢复, True: 处于异常中
    6: double minimum,          // 异常记录的下限
    7: double maximum,          // 异常记录的上限
}

// 节点上已安装的服务
struct ncTNodeServer {
    1: string uuid,                     // 节点uuid
    2: list<string> services,         // 杀毒服务
}

// 错误码
enum ncTECMSManagerError {
    NCT_INVALID_ACCOUNT_OR_PASSWORD = 10001,        // 用户账号或密码不正确
    NCT_NODE_ALREADAY_IN_CLUSTER = 10002,           // 节点已在集群中
    NCT_NIC_NOT_AVAILABLE = 10003,                  // 网卡不存在
    NCT_SSH_TO_REMOTE_HOST_FAILED = 10004,          // 通过 ssh 连接远程主机失败
    NCT_EXTERNAL_DB_NOT_AVAILABLE = 10005,          // 测试第三方数据库不可用
    NCT_NODE_IS_OFFLINE = 10006,                    // 节点离线
    NCT_NO_APPLICATION_NODE = 10007,                // 没有应用节点
    NCT_NO_AVAILABLE_APPLICATION_NODE = 10008,      // 没有可用的应用节点

    NCT_INVALID_ARGUMENT = 20001,                   // 参数错误
    NCT_INTERNAL_ERROR = 20002,                     // 内部错误
    NCT_NOT_IN_SAME_SUNNET = 20006,                 // 非同网段错误

    NCT_NOT_APPLICATION_NODE = 30001,               // 当前节点不是应用节点
    NCT_SERVICE_PACKAGE_MISSING = 30002,            // 没有可用的服务安装包
    NCT_SERVER_ALREADY_INSTALLED = 30003,           // 服务已经安装
    NCT_SERVER_NOT_INSTALLED = 30004,               // 服务未安装
}


/**
 * ECMSManager thift 管理接口
 */
service ncTECMSManager {

    /////////////////////////////////////////////////////////////////
    // 1、集群部署 ecms manager
    /////////////////////////////////////////////////////////////////

    /**
     * 节点环境是否干净
     * @param   <string>    host    节点 IP 地址
     * @param   <i32>       port    SSH 端口
     * @param   <string>    user    SSH 用户
     * @param   <string>    passwd  SSH 密码
     * @return  <bool>                          True:   节点环境不干净
     *                                          False:  节点环境干净
     */
    bool is_node_dirty(
        1: string host,
        2: i32 port,
        3: string user,
        4: string passwd,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 检查节点环境是否干净
     * 前提：可以连通被检查节点，开放了集群管理服务的访问端口
     * @param   <string>    node_ipaddr    节点 IP 地址
     * @return  <bool>                          True:   节点环境不干净
     *                                          False:  节点环境干净
     */
    bool is_env_dirty(1: string node_ipaddr)
        throws(1: EThriftException.ncTException exp),

    /**
     * 清理节点
     * @param   <string>    node_ipaddr         节点 IP 地址
     */
    void clear_node(1: string node_ipaddr)
        throws(1: EThriftException.ncTException exp),

    /**
     * 激活集群
     * @param   <string>    node_ipaddr         节点 IP 地址
     * @return  <string>                        集群 UUID
     */
    string active_cluster(1: string node_ipaddr)
        throws(1: EThriftException.ncTException exp),

    /**
     * 添加节点
     * @param   <string>    host    节点 IP 地址
     * @return  <string>            节点 UUID
     */
    string add_node(1: string host)
        throws(1: EThriftException.ncTException exp),

    /**
     * 移除节点
     * @param   <string>    node_uuid   节点 UUID
     */
    void del_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取模块状态
     * @param   <string>    module_name  模块名
     */
    bool get_module_status(1: string module_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用模块
     * @param   <string>    module_name  模块名
     */
    void enable_module(1: string module_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用模块
     * @param   <string>    module_name  模块名
     */
    void disable_module(1: string module_name)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 2、数据库管理 mysql manager
    /////////////////////////////////////////////////////////////////

    /**
     * 创建ecms集群管理数据库
     */
    void create_ecms_db()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取数据库节点信息
     * @return list<ncTDBNodeInfo> 数据库节点信息列表
     */
    list<ncTDBNodeInfo> get_db_node_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置数据库主库
     * @param <string>      node_uuid 节点ID
     */
    void set_db_master(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置数据库备份从节点
     * @param <string>      node_uuid 节点ID
     */
    void set_db_slave(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置数据库备份从节点,根据空间大小自动判断使用xtrabackup备份方式或者mysqldump
     * @param <string>      node_uuid 节点ID
     * @param ECMSAgent.ncTSSHInfo slave_ssh_info  数据库高可用备份从节点 ssh 信息
     *        ncTSSHInfo.host     : 主机地址
     *        ncTSSHInfo.port     : 连接端口
     *        ncTSSHInfo.user     : ssh 用户
     *        ncTSSHInfo.password : ssh 密码
     */
    void set_db_slave_by_xtrabackup(1: string node_uuid, 2: ECMSAgent.ncTSSHInfo slave_ssh_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 移出数据库节点
     * @param <string>      node_uuid 节点ID
     */
    void cancel_db_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新集群部署模式
     * @param <string>   mode 部署模式 NCT_STANDARD_MODE
     *                                 NCT_PROFESSIONAL_MODE
     */
    void update_deployment_mode(1: string mode)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取集群部署模式
     */
    string get_deployment_mode()
        throws(1: EThriftException.ncTException exp),

    /**
     * 使用mysqldump导出数据到指定目录
     * @param <string> host 数据库地址
     * @param <int> port 数据库端口
     * @param <string> db_name 数据库名
     * @param <string> path 导出目录绝对路径
     */
    void dump_databases_to_path(1: string host,
                                2: i32 port,
                                3: string db_name,
                                4: string path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取数据库名
     * 注:过滤了"information_schema", "mysql", "performance_schema", "sys"数据库
     * @param <string> host 数据库地址
     * @param <int> port 数据库端口
     * @return list<string> 数据库名称列表
     */
    list<string> get_databases_name(1: string host,
                                    2: i32 port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 移除指定数据库节点的binlog文件
     * @param <string> 节点uuid
     */
    void purge_binlogs(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新第三方数据库信息
     * @param ncTExternalDBInfo info 第三方数据库信息
     *        ncTExternalDBInfo.db_host:第三方数据库地址,
     *        ncTExternalDBInfo.db_port:第三方数据库端口,
     *        ncTExternalDBInfo.db_user:第三方数据库用户,
     *        ncTExternalDBInfo.db_password:第三方数据库密码
     */
    void update_external_db_info(1: ECMSAgent.ncTExternalDBInfo info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取第三方数据库信息
     * @return <ncTExternalDBInfo> 第三方数据库连接结构,结构属性同上
     */
    ECMSAgent.ncTExternalDBInfo get_external_db_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 判断是否使用第三方数据库
     */
    bool is_external_db()
        throws(1: EThriftException.ncTException exp),

    /**
     * 测试第三方数据库是否可用
     * @return <bool> True:可用 | False 不可用
     */
    bool is_available_external_db(1: ECMSAgent.ncTExternalDBInfo info)
        throws(1: EThriftException.ncTException exp),


    /////////////////////////////////////////////////////////////////
    // 3、防火墙管理 firewall manager
    /////////////////////////////////////////////////////////////////

    /**
     * 添加防火墙规则
     * @param <ncTFirewallInfo> firewall_info 待添加防火墙信息结构
     */
    void add_firewall_rule(1: ncTFirewallInfo firewall_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除防火墙规则
     * @param <ncTFirewallInfo> firewall_info 待删除防火墙信息结构
     */
    void del_firewall_rule(1: ncTFirewallInfo firewall_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 修改防火墙规则
     * @param <ncTFirewallInfo> old_info 待修改防火墙信息结构
     * @param <ncTFirewallInfo> new_info 修改后防火墙信息结构
     */
    void update_firewall_rule(1: ncTFirewallInfo old_info,
                              2: ncTFirewallInfo new_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定子系统所有防火墙规则
     * param <string> sys_role 规则所属的子系统,参数如下
     *                         db:      数据库子系统
     *                         app:     应用子系统
     *                         ecms:    集群管理子系统
     *                         basic:   基础规则,所有节点应用
     *                         storage: 存储子系统
     * return list<ncTFirewallInfo> 防火墙结构信息列表
     */
    list<ncTFirewallInfo> get_firewall_rule(1: string sys_role)
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用集群防火墙
     */
    void enable_firewall()
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用集群防火墙
     */
    void disable_firewall()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取集群防火墙状态
     * return bool True:  防火墙开启
                   False: 防火墙关闭
     */
    bool get_firewall_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 允许子系统对外服务
     * param <string> sys_role 规则所属的子系统,参数及含义如下
     *                         db:      数据库子系统
     *                         app:     应用子系统
     *                         ecms:    集群管理子系统
     *                         basic:   基础规则,所有节点应用
     *                         storage: 存储子系统
     */
    void enable_sys_service(1: string sys_role)
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁止子系统对外服务
     * param <string> sys_role 规则所属的子系统,参数及含义如下
     *                         db:      数据库子系统
     *                         app:     应用子系统
     *                         ecms:    集群管理子系统
     *                         basic:   基础规则,所有节点应用
     *                         storage: 存储子系统
     */
    void disable_sys_service(1: string sys_role)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取子系统对外服务状态
     * param <string> sys_role 规则所属的子系统,参数及含义如下
     *                         db:      数据库子系统
     *                         app:     应用子系统
     *                         ecms:    集群管理子系统
     *                         basic:   基础规则,所有节点应用
     *                         storage: 存储子系统
     * return bool True:       允许子系统对外服务
                   False:      禁止子系统对外服务
     */
    bool get_sys_service_status(1: string sys_role)
        throws(1: EThriftException.ncTException exp),

    /*
     * 添加集群内部的信任ip
     * @param list<string> ip列表
     */
    void add_trusted_ip(1: list<string> ip_list)
        throws(1: EThriftException.ncTException exp),

    /*
     * 设置本地存储（Ceph）的信任 IP 规则，覆盖原有规则
     * @param list<ncTFirewallInfo> firewall_list 防火墙规则列表
     */
    void set_storage_trusted_ip(1: list<ncTFirewallInfo> firewall_list)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取指定节点上放行的asu ip
     * @param return list<string> ip列表
     */
    list<string> get_asu_node_ip()
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 4、高可用管理
    /////////////////////////////////////////////////////////////////

    /**
     * 获取高可用模块启用状态
     * @return  bool    True:   启用
     *                  False:  禁用
     **/
    bool get_keepalived_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用高可用模块
     **/
    void enable_keepalived()
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用高可用模块
     **/
    void disable_keepalived()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取高可用vip信息列表
     * @return <ncTVipInfo> vip信息结构
     */
    list<ncTVipInfo> get_vip_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 修改高可用vip信息
     * @param <ncTVipInfo> 待设置的vip信息结构
     * 例: ncTVipInfo(vip='192.168.136.1', nic='ens32', mask='255.255.255.0', sys=ncTHaSys.BASIC)
     */
    void set_vip_info(1: ncTVipInfo vip_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 修改高可用ivip信息
     * @param <ncTVipInfo> 待设置的ivip信息结构
     */
    void set_ivip_info(1: ncTVipInfo ivip_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取所有的ha节点信息
     * @return list<ncTHaNodeInfo> 高可用节点信息列表
     */
    list<ncTHaNodeInfo> get_ha_node_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置高可用主节点
     * @param <string>      node_uuid 节点ID
     * @param <ncTVipInfo>  vip_info  vip信息结构
     * 例1：单vip方案, vip参数如下, sys为标记高可用节点所属子系统
     * ncTVipInfo(vip='192.168.136.1', nic='ens32', mask='255.255.255.0', sys=ncTHaSys.BASIC)
     * 例2：多vip方案，设置应用子系统高可用
     * ncTVipInfo(vip='192.168.136.1', nic='ens32', mask='255.255.255.0', sys=ncTHaSys.APP)
     */
    void set_ha_master(1: string node_uuid,
                       2: ncTVipInfo vip_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置高可用从节点
     * @param <string>      node_uuid 节点ID
     * @param <int>    ha_sys 所属高可用系统标记,参数使用如下值:
     *                             ncTHaSys.BASIC   集群使用一个vip方案使用值
     *                             ncTHaSys.APP     应用高可用
     *                             ncTHaSys.STORAGE 存储高可用
     */
    void set_ha_slave(1: string node_uuid,
                      2: i32 ha_sys)
        throws(1: EThriftException.ncTException exp),

    /**
     * 取消高可用节点
     * @param <string>      node_uuid 节点ID
     */
    void cancel_ha_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置数据库高可用主
     * @param <ncTVipInfo>      ivip_info 数据库ivip
     */
    void set_db_ha_master(1: ncTVipInfo ivip_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置数据库高可用从
     */
    void set_db_ha_slave()
        throws(1: EThriftException.ncTException exp),

    /**
     * 取消数据库高可用
     * @param <string>      node_uuid 节点ID
     */
    void cancel_db_ha_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新lvs
     */
    void on_lvs_changed()
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // ！以下接口用于高可用切换管理，仅限当前节点调用
    /**
     * 高可用节点进入主
     */
    void on_node_entering_master()
        throws(1: EThriftException.ncTException exp),

    /**
     * 高可用节点进入从
     */
    void on_node_entering_slave()
        throws(1: EThriftException.ncTException exp),

    /**
     * 将当前节点临时地强制切换为主节点(慎用！)
     * 下次keepalived启动时生效，仅一次有效
     * PS：强制切换时，会忽略数据库的binlog IO同步状态
     */
    void force_enter_master()
        throws(1: EThriftException.ncTException exp),


    /////////////////////////////////////////////////////////////////
    // 5、节点管理 node manager
    /////////////////////////////////////////////////////////////////

    /**
     * 获取指定节点信息
     * @param string node_uuid 节点uuid
     * @return <ncTNodeInfo> 节点信息
     */
    ncTNodeInfo get_node_info(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取所有节点信息
     * @return list<ncTNodeInfo> 节点信息列表
     */
    list<ncTNodeInfo> get_all_node_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置节点别名
     * @param string node_uuid 节点uuid
     * @param string node_alias 节点别名
     */
    void set_node_alias(1: string node_uuid,
                        2: string node_alias)
        throws(1: EThriftException.ncTException exp),

    /**
     * 指定节点异步重启eisooapp服务
     * @param string node_uuid 节点uuid
     */
    void restart_eisooapp(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 重启指定节点
     * @param string node_uuid 节点uuid
     */
    void reboot_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 关闭集群所有节点
     */
    void shutdown_cluster()
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下为获取集群信息

    /**
     * 获取集群时间
     * @return i64 当前集群系统时间UNIX时间戳
     */
    i64 get_cluster_time()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置集群时间
     * 时间格式："yyyy-mm-dd hh:mm:ss"
     * @param string datetime 待设置时间
     */
    void set_cluster_time(1: string datetime)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取集群版本
     * @return string 当前集群使用的 AnyShare Server 包版本号
     * 如安装的 Server 包名为AnyShare-Server-6.0.1-20170511-81,则返回值为 "6.0.1-20170511-81"
     */
    string get_cluster_version()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取集群 uuid
     * @return string 集群 uuid, 集群唯一标识
     */
    string get_cluster_uuid()
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下为设置日志推送功能相关接口

    /**
     * 添加一台远程日志服务器,若推送功能开启则立即生效
     * @param str facility: 接收规则模块
     *            参数: kern, user, mail, daemon, auth, syslog, lpr, news, uucp, authpriv,
     *                  ftp, cron, local0, local1, local2, local3, local4, local5, local6, local7
     * @param str severity: 接收规则等级
     *            参数: emerg, alert, crit, err, warn, notice, info, debug
     * @param string ip: 远程服务器ip地址
     * @param int port: 远程服务器端口
     * @param string protocol：传输协议TCP/UDP
     */
    void add_log_server(1: string facility,
                        2: string severity,
                        3: string ip,
                        4: i32 port
                        5: string protocol)
            throws(1: EThriftException.ncTException exp),

    /**
     * 删除一台日志服务器,若推送功能开启则立即生效
     * @param str facility: 接收规则模块
     * @param str severity: 接收规则等级
     * @param string ip: 远程服务器ip地址
     * @param int port: 远程服务器端口
     * @param string protocol：传输协议TCP/UDP
     */
    void delete_log_server(1: string facility,
                           2: string severity,
                           3: string ip,
                           4: i32 port
                           5: string protocol)
    throws(1: EThriftException.ncTException exp),

    /**
     * 开启日志推送到日志服务器功能
     * @param str datetime 用户日志推送起始时间
     *  e.g: 2016-06-20 09:00:00
     */
    void enable_upload_log(1: string datetime)
        throws(1: EThriftException.ncTException exp),

    /**
     * 关闭日志推送到日志服务器功能
     */
    void disable_upload_log()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取日志推送到日志服务器功能状态
     * return bool False 日志推送服务关闭
     *             True  日志推送服务开启
     */
    bool get_upload_log_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取数据库中日志服务器信息列表
     * @return list<ECMSAgent.ncTLogHostInfo>
     */
    list<ECMSAgent.ncTLogHostInfo> get_upload_log_server()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取用户日志推送起始时间的UNIX时间戳
     * @return int UNIX时间戳
     */
    i32 get_upload_log_time()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点的所有网卡名
     */
    list<string> get_all_nics_name(1:string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 界面获取节点系统信息接口

    /**
     * 获取指定节点cpu使用率
     * @param <string> node_uuid 节点uuid
     * @return <double> cpu使用率
     */
    double get_cpu_usage(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点内存使用情况
     * @param <string> node_uuid 节点uuid
     * @return map<string, i64> {'usage': 已用内存B, 'total': 总共内存B}
     */
    map<string, i64> get_memory_info(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取网络发送速率
     * @param <string> node_uuid 节点uuid
     * @return <int> 网络发送速度 B/s
     */
    i64 get_network_outgoing_rate(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),
    /**
     * 获取网络接收速度
     * @param <string> node_uuid 节点uuid
     * @return <int> 网络接收速度 B/s
     */
    i64 get_network_incoming_rate(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口用于故障处理，仅限当前节点调用

    /**
     * 对当前节点环境进行故障检测及处理
     * 故障如：服务停止
     */
    void troubleshoot()
        throws(1: EThriftException.ncTException exp),

    /**
     * 对当前节点环境进行一致性检测及处理
     */
    void consistency_repair()
        throws(1: EThriftException.ncTException exp),

    /**
     * 对当前节点环境进行一致性检测
     * 若节点各子模块均与集群保持一致(不需要进行一致性恢复), 返回 True
     * 若节点各子模块中存在任一模块与集群状态不一致(则需要进行一致性恢复), 返回 False
     */
    bool consistency_check()
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口用于节点心跳更新

    /**
     * 收到节点心跳的处理
     * @param <string> node_uuid 节点uuid
     */
    void on_node_heartbeat(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口用于节点 ip 变更时调用，本节点调用

    /**
     * 手动修改节点 ip 后，调用该接口更新相关元数据等信息
     * @param <string> old_ip 原 ip
     * @param <string> new_ip 新 ip
     * @param <bool>   update_db_host 如果待更新的节点原 ip 用于数据库连接，
     *                                需要通过该接口更新各节点的 db_host
     *                                信息，为 True；否则为 False
     *                                调用时，需要能连通各节点的 agent
     */
    void on_change_node_ip(1: string old_ip,
                           2: string new_ip,
                           3: bool update_db_host)
        throws(1: EThriftException.ncTException exp),


    /////////////////////////////////////////////////////////////////
    // 6、存储管理 storage manager
    /////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////
    // 以下接口用于存储池设备管理

    /**
     * 启用 raid 管理模块, 默认不支持 raid 管理, 只有 eisoo 一体机设备并且指定型号 raid 卡才支持
     */
    void enable_raid_manager()
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用 raid 管理模块
     */
    void disable_raid_manager()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取raid管理模块启用状态
     */
    bool get_raid_manager_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 是否支持raid管理
     * @param string node_ip 节点ip
     * @return bool True:  支持raid管理
     *              False: 不支持raid管理
     */
    bool is_available_of_raid_manager(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
    * 判断节点是否存在外挂存储
    * @param string node_ip          节点的node_ip
    */
    bool exist_iscsi_device(1: string node_ip)
        throws(1: EThriftException.ncTException exp)

    /**
     * 获取指定节点上的空闲数据盘
     * 空闲数据盘：指尚未加入存储池的数据盘
     *
     * @param string node_ip                    节点的 node_ip
     * @return map<disk_dev_path, data_disk>    空闲数据盘列表
     */
    map<string, ECMSAgent.ncTDataDisk> get_free_data_disks(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 初始化存储池
     *
     * @param int replicas 副本数
     */
    void init_storage_pool(1: i32 replicas)
        throws(1: EThriftException.ncTException exp),

    /**
     * 判断存储池是否已初始化
     */
    bool is_storage_pool_inited()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取存储池信息
     *
     * @param bool need_used_size       是否包含已用空间
     *      若为True，则需要从各个节点查询所有磁盘的可用空间情况，当节点数较多时，花费时间将较长
     */
    ncTStoragePool get_storage_pool(1: bool include_used_size)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取存储池中指定节点上的设备列表(包含设备对应的数据卷信息)
     *
     * @param string node_ip          节点的ip, 若为""，则获取全部节点
     * @return map<ECMSAgent.ncTSwiftDevice.dev_id, ncTStoragePoolDevice>
     */
    map<i32, ncTStoragePoolDevice> get_storage_pool_devices(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取存储池中swift设备列表(按节点分组，不包含设备对应的数据卷信息)
     *
     * @return map<node_ip, map<ECMSAgent.ncTSwiftDevice.dev_id, ncTStoragePoolDevice> >
     */
    map<string, map<i32, ECMSAgent.ncTSwiftDevice> > get_storage_pool_swift_devices()
        throws(1: EThriftException.ncTException exp),

    /**
     * 将指定节点上的指定空闲数据盘一次性加入到存储池中
     *
     * @param disks(map<node_ip, list<disk_dev_path>>)  空闲数据盘列表，由 get_free_data_disks 可知
     */
    void add_devices_to_pool(1: map<string, list<string>> disk_dev_paths)
        throws(1: EThriftException.ncTException exp),

    /**
     * 将指定某一节点的所有空闲数据盘一次性加入到存储池中
     *
     * @param string node_ip      节点 ip
     */
    void add_node_devices_to_pool(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定存储池设备的维护状态
     * @param   list<string>    dev_uuids   指定存储池设备的 UUID 列表
     * @return  list<bool>                  True: 处于维护状态
     *                                      False: 未处于维护状态
     */
    list<bool> get_maintenance_of_devices(1: list<string> dev_uuids)

    /**
     * 指定存储池设备进入维护状态
     * @param   list<string>    dev_uuids   指定存储池设备的 UUID 列表
     * @return  list<string>    dev_uuids   进入维护模式的 UUID 列表
     */
    list<string> enable_maintenance_of_devices(1: list<string> dev_uuids)

    /**
     * 指定存储池设备退出维护状态
     * @param   list<string>    dev_uuids   指定存储池设备的 UUID 列表
     * @return  list<string>    dev_uuids   退出维护模式的 UUID 列表
     */
    list<string> disable_maintenance_of_devices(1: list<string> dev_uuids)

    /**
     * 获取可用于替换指定存储池设备的备选空闲数据盘列表
     * 规则：
     *   1.备选设备和要替换的设备处于同一服务器节点
     *
     * @param dev_id(int)     存储池中需要被替换的设备ID， ncTStoragePoolDevice.swift_device.dev_id
     * @return map<disk_dev_path, data_disk>   备选空闲数据盘列表
     */
    map<string, ECMSAgent.ncTDataDisk> get_free_data_disks_for_replace(1: i32 dev_id)
        throws(1: EThriftException.ncTException exp),

    /**
     * 在存储池中使用指定数据盘替换指定存储池设备（仅限同一节点内的磁盘替换）
     * 单副本环境不支持此操作
     * 若替换磁盘的容量与原磁盘不一致，则此操作会引起存储池内的数据重新负载均衡及迁移
     * 此操作适用于某块故障卷可以被尽快更换的场景，或需要替换使用大容量磁盘达到扩容目的的场景
     *
     * @param dev_id(int)           存储池中需要被替换的设备ID， ncTStoragePoolDevice.swift_device.dev_id
     * @param disk_dev_path(str)    用于替换的数据盘路径
     */
    void replace_device_in_pool(1: i32 dev_id, 2: string disk_dev_path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 从存储池中移除单个设备
     * 此操作会引起存储池内的数据重新负载均衡及迁移
     * 此操作适用于某块存储卷已故障不可用，且长时间无法得到恢复或更换的场景
     * 单副本环境不支持此操作
     *
     * @param dev_id(int)   存储池中的设备ID， ncTStoragePoolDevice.swift_device.dev_id
     */
    void remove_device_from_pool(1: i32 dev_id)
        throws(1: EThriftException.ncTException exp),

    /**
     * 从存储池中移除指定节点的所有设备
     * 单副本环境不支持此操作
     *
     * @param string node_ip      节点 ip
     */
    void remove_node_devices_from_pool(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 将存储池重新负载均衡
     */
    void rebalance_storage_pool()
        throws(1: EThriftException.ncTException exp),

    /**
     * 修改存储池副本数
     *
     * @param int replicas 副本数
     */
    void change_replicas(1: i32 replicas)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口用于存储池健康状态管理

    /**
     * 查询当前存储池的副本健康度.
     * 内部采用抽样的方法检测.
     * @return health_percent   返回健康百分比之分子，等于 100 可视为健康，
     *                          说明所有对象的副本都100%存在正确的位置上。
     */
    double get_replicas_health()
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口用于RAID设备管理

    /**
     * 获取指定节点上的所有数据RAID物理磁盘列表
     *
     * @param string node_ip                    节点 ip
     * @return map<pd_devid, pdinfo>            RAID物理磁盘列表
     */
    map<string, ECMSAgent.ncTRaidPDInfo> get_all_data_raid_pds(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点上的空闲数据RAID物理磁盘列表
     * 空闲数据RAID物理磁盘：指尚未加入存储池的数据RAID物理磁盘
     *
     * @param string node_ip                    节点 ip
     * @return map<pd_devid, pdinfo>            RAID物理磁盘列表
     */
    map<string, ECMSAgent.ncTRaidPDInfo> get_free_data_raid_pds(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点上的已加入存储池的数据RAID物理磁盘列表
     *
     * @param string node_ip                    节点 ip
     * @return map<pd_devid, pdinfo>            RAID物理磁盘列表
     */
    map<string, ECMSAgent.ncTRaidPDInfo> get_raid_pds_in_storage_pool(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点上的系统RAID物理磁盘列表
     * 系统RAID物理磁盘：指用于系统盘或缓存盘的RAID物理磁盘或热备盘
     *
     * @param string node_ip                    节点 ip
     * @return map<pd_devid, pdinfo>            RAID物理磁盘列表
     */
    map<string, ECMSAgent.ncTRaidPDInfo> get_sys_raid_pds(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点上的所有RAID逻辑磁盘列表
     *
     * @param string node_ip                    节点 ip
     * @return map<ld_devid, ldinfo>            RAID逻辑磁盘列表
     */
    map<string, ECMSAgent.ncTRaidLDInfo> get_all_raid_lds(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 查询指定节点的指定 RAID 物理磁盘设备的详细信息
     *
     * @param string node_ip       节点 ip
     * @param string pd_devid:     设备唯一标识
     * @return map<key, value>:    RAID 物理磁盘设备的详细信息
     */
    map<string, string> get_raid_pd_details(1: string node_ip, 2: string pd_devid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 查询指定节点的指定 RAID 逻辑磁盘设备的详细信息
     *
     * @param string node_ip       节点 ip
     * @param string ld_devid:     设备唯一标识
     * @return map<key, value>:    RAID 逻辑设备的详细信息
     */
    map<string, string> get_raid_ld_details(1: string node_ip, 2: string ld_devid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 初始化指定节点上的指定空闲数据RAID物理磁盘
     * 空闲数据RAID物理磁盘：指尚未加入存储池的数据RAID物理磁盘
     *
     * @param string node_ip            节点 ip
     * @param list<pd_devid> pd_devids  需要初始化的RAID物理磁盘设备列表
     * @param int bond_disks_num        指定将几个磁盘绑定为一个数据盘
     *                                  == 1：表示使用一个磁盘，对应一个数据盘
     *                                  > 1：通常用于单副本，需要做RAID5的环境，将 n 个磁盘组合成一个数据盘
     *                                  PS：> 1 仅对RAID环境生效，裸磁盘均默认按 == 1 处理.
     * @return map<ld_devid, ldinfo>    返回初始化创建的RAID逻辑卷列表
     */
    map<string, ECMSAgent.ncTRaidLDInfo> init_free_data_raid_pds(
        1: string node_ip,
        2: list<string> pd_devids,
        3: i32 bond_disks_num)
        throws(1: EThriftException.ncTException exp),

    /**
     * 在指定节点上添加RAID热备盘
     *
     * @param string node_ip        节点 ip
     * @param string pd_devid       热备盘ID，可从空闲数据RAID物理磁盘中选取
     * @param string ld_devid       指定需要添加热备盘的RAID逻辑磁盘设备ID，若为空，则添加为全局热备盘
     */
    void add_raid_hotspare(
        1: string node_ip,
        2: string pd_devid,
        3: string ld_devid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 在指定节点上删除热备盘
     *
     * @param string node_ip        节点 ip
     * @param string pd_devid       热备盘ID
     */
    void remove_raid_hotspare(
        1: string node_ip,
        2: string pd_devid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点上的可添加热备盘的RAID逻辑磁盘列表
     *
     * @param string node_ip                    节点 ip
     * @return map<ld_devid, ldinfo>            RAID逻辑磁盘列表
     */
    map<string, ECMSAgent.ncTRaidLDInfo> get_raid_lds_for_hotspare(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口用于缓存卷管理

    /**
     * 在指定数据盘上创建缓存卷
     *
     * @param disk_dev_path(str)    指定磁盘在系统中的设备路径
     * @return vol_dev_path(str)    返回所创建的缓存卷设备路径
     */
    string create_cache_volume(1: string node_uuid,
                               2: string disk_dev_path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除缓存卷
     */
    void remove_cache_volume(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取缓存卷信息
     * return ECMSAgent.ncTVolume: 缓存卷信息
     */
    ECMSAgent.ncTVolume get_cache_volume(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 初始化缓存卷
     * 若缓存卷存在，则：清除缓存卷及缓存目录中的数据，并挂载
     * 若缓存卷不存在，则：清除缓存目录中的数据
     */
    void init_cache_volume(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 判断缓存卷是否已初始化
     * 若缓存卷存在，若缓存卷中无数据，且已挂载，则已初始化
     * 若缓存卷不存在，若缓存目录存在，且无数据，则未初始化
     */
    bool is_cache_volume_inited(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 挂载缓存卷
     * 若缓存卷不存在，则忽略
     * 若缓存卷挂载失败，则记日志
     */
    void mount_cache_volume(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 为各应用分配缓存卷
     */
    void allocate_cache_volume(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 获取磁盘信息

    /**
     * @param <string> node_uuid 节点uuid
     * @return ECMSAgent.ncTVolume 系统卷相关信息
     * 获取指定节点系统卷信息
     */
    ECMSAgent.ncTVolume get_sys_volume(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * @param <string> node_uuid 节点uuid
     * @return ECMSAgent.ncTVolume sysvol卷相关信息
     * 获取指定节点系统卷信息
     */
    ECMSAgent.ncTVolume get_sysvol_volume(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点上指定磁盘的信息
     * @param <string> node_uuid 节点uuid
     * @param map<string, string> 指定磁盘相关信息
     */
    map<string, string> get_disk_info(1: string node_uuid,
                                      2: string dev_path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点上所有数据盘
     * @param string node_uuid 节点uuid
     * @return data_disks(map<disk_dev_path, ncTDataDisk>)        返回数据盘列表
     */
    map<string, ECMSAgent.ncTDataDisk> get_data_disks(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 获取存储（本地Ceph）控制台登录地址

    /**
     * 获取存储（本地Ceph）控制台登录地址
     * @param string       storage_server_name Ceph 对象存储访问地址
     * @return string      Ceph 控制台登录地址
     */
    string get_storage_console_address(1: string storage_server_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取本地Ceph存储的容量信息
     * @param string       storage_server_name Ceph 对象存储访问地址
     * @return ncTCephStorageInfo
     */
    ncTCephStorageInfo get_local_ceph_storage_info(1: string storage_server_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置存储（本地Ceph）管理vip
     * @param string       ceph_manage_vip Ceph 管理vip
     *                     参数可以是ip或者域名，接口内不做检查
     */
    void set_local_ceph_manage_vip(1: string ceph_manage_vip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取存储（本地Ceph）管理vip
     * @return string      ceph_manage_vip Ceph 管理vip
     */
    string get_local_ceph_manage_vip()
        throws(1: EThriftException.ncTException exp),


    /////////////////////////////////////////////////////////////////
    // 7、监控告警管理
    /////////////////////////////////////////////////////////////////

    /**
     * 获取监控服务状态
     * @return  bool    True:   启用
     *                  False:  禁用
    **/
    bool get_zabbix_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用 zabbix
     * 初始化数据库, 导入配置, 创建主机, 链接模板
     **/
    void enable_zabbix()
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用 zabbix
     * 停止服务
     **/
    void disable_zabbix()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取告警项状态
     * @return map<string, bool>
     *                                  string: 触发器分类
     *                                  i32:
                                            1:  触发器正常
                                            0:  触发器异常
                                            -1: 对应监控不存在
     */
    map<string, i32> get_alert_trigger_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取告警通知开关状态
     * @return  bool                    True: 开启, False: 关闭
     */
    bool is_alert_enable()
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用告警通知
     */
    void enable_alert()
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用告警通知
     */
    void disable_alert()
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用监控维护模式
     */
    void enable_maintenance()
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用监控维护模式
     */
    void disable_maintenance()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取监控维护模式状态
     * @return bool False : 维护模式禁用
     *              True  : 维护模式启用
     */
    bool get_maintenance_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取系统服务异常记录
     * @param string ipaddr 节点的 IP 地址
     * @param i32 time_from 返回指定时间之后的记录
     * @param i32 time_till 返回指定时间之前的记录
     * @return list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_service_problem_records(
        1: string ipaddr,
        2: i32 time_from,
        3: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取数据库异常记录
     * @param string ipaddr 节点的 IP 地址
     * @param i32 time_from 返回指定时间之后的记录
     * @param i32 time_till 返回指定时间之前的记录
     * @return list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_database_problem_records(
        1: string ipaddr,
        2: i32 time_from,
        3: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取 CPU 异常记录
     * @param string ipaddr 节点的 IP 地址
     * @param double threshold CPU 负载阈值, 高于阈值则认为异常
     * @param i32 time_from 返回指定时间之后的记录
     * @param i32 time_till 返回指定时间之前的记录
     * @return list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_cpu_problem_records(
        1: string ipaddr,
        2: double threshold,
        3: i32 time_from,
        4: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取系统卷异常记录
     * @param string ipaddr 节点的 IP 地址
     * @param i32 time_from 返回指定时间之后的记录
     * @param i32 time_till 返回指定时间之前的记录
     * @return list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_sysvol_problem_records(
        1: string ipaddr,
        2: i32 time_from,
        3: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取内存异常记录
     * @param   string  ipaddr      节点的 IP 地址
     * @param   double  threshold   内存负载阈值, 高于阈值则认为异常
     * @param   i32     time_from   返回指定时间之后的记录
     * @param   i32     time_till   返回指定时间之前的记录
     * @return  list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_memory_problem_records(
        1: string ipaddr,
        2: double threshold,
        3: i32 time_from,
        4: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取系统自备份异常记录
     * @param   string  ipaddr      节点的 IP 地址
     * @param   i32     time_from   返回指定时间之后的记录
     * @param   i32     time_till   返回指定时间之前的记录
     * @return  list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_self_backup_problem_records(
        1: string ipaddr,
        2: i32 time_from,
        3: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取节点在线状态异常记录
     * @param   string  ipaddr      节点的 IP 地址
     * @param   i32     time_from   返回指定时间之后的记录
     * @param   i32     time_till   返回指定时间之前的记录
     * @return  list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_node_online_problem_records(
        1: string ipaddr,
        2: i32 time_from,
        3: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取节点切换异常记录
     * @param   string  ipaddr      节点的 IP 地址
     * @param   i32     time_from   返回指定时间之后的记录
     * @param   i32     time_till   返回指定时间之前的记录
     * @return  list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_node_switch_problem_records(
        1: string ipaddr,
        2: i32 time_from,
        3: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取对象存储副本健康度异常记录
     * 副本健康度非 100.0% 为异常
     * @param string ipaddr 节点的 IP 地址
     * @param i32 time_from 返回指定时间之后的记录
     * @param i32 time_till 返回指定时间之前的记录
     * @return list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_replicas_problem_records(
        1: string ipaddr,
        2: i32 time_from,
        3: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取存储池设备异常记录
     * @param   string  ipaddr      节点的 IP 地址
     * @param   i32     time_from   返回指定时间之后的记录
     * @param   i32     time_till   返回指定时间之前的记录
     * @return  list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_storage_dev_problem_records(
        1: string ipaddr,
        2: i32 time_from,
        3: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取对象存储负载均衡异常记录
     * 负载均衡小于 0 为异常
     * @param string ipaddr 节点的 IP 地址
     * @param i32 time_from 返回指定时间之后的记录
     * @param i32 time_till 返回指定时间之前的记录
     * @return list<ncTMonitorProblemRecord>
     */
    list<ncTMonitorProblemRecord> get_balance_problem_records(
        1: string ipaddr,
        2: i32 time_from,
        3: i32 time_till,
    )
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 8、节点角色管理
    /////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////
    // 存储节点角色

    /**
     * 添加存储节点
     * @param string node_uuid 节点uuid
     */
    void add_storage_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 移除存储节点
     * @param string node_uuid 节点uuid
     */
    void del_storage_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取存储节点信息
     */
    list<ncTStorageNodeInfo> get_storage_node_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取存储子系统主节点 ip
     * 存储主节点，只是按照一定规则获取的一个在线的存储节点
     * 注意：接口不拋错, 若没有查找到可用节点ip,返回为空字符串""
     * @return  <string> ip
     */
    string get_storage_master_node_ip()
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用指定节点的存储lvs
     * @param string node_uuid 节点uuid
     */
    void enable_storage_lvs(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用指定节点的存储lvs
     * @param string node_uuid 节点uuid
     */
    void disable_storage_lvs(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 应用节点角色

    /**
     * 添加应用节点
     * @param node_uuid 节点uuid
     */
    void add_application_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 移除应用节点
     * @param node_uuid 节点uuid
     */
    void del_application_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取应用节点信息
     */
    list<ncTAppNodeInfo> get_app_node_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取应用子系统主节点
     * @return  ncTAppNodeInfo  应用节点信息
     */
    ncTAppNodeInfo get_app_master_node_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取应用子系统主节点 ip
     * 注意：接口不拋错, 若没有查找到可用节点ip,返回为空字符串""
     * @return  <string> ip
     */
    string get_app_master_node_ip()
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用指定节点的应用lvs
     * @param   string  node_uuid  节点uuid
     */
     void enable_app_lvs(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用指定节点的应用lvs
     * @param   string  node_uuid   节点uuid
     */
     void disable_app_lvs(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),


    /////////////////////////////////////////////////////////////////
    // 9、应用服务管理
    /////////////////////////////////////////////////////////////////

    /**
     * 获取所有应用服务
     * @return  list<ncTAppServiceInfo>
     */
    list<ncTAppServiceInfo> get_application_service()
        throws(1: EThriftException.ncTException exp),

    /**
     * 添加应用服务
     * @param string service_name 服务名
     * @param i32    port         端口
     * @param bool   is_lvs       是否进行端口转发
     */
    void add_application_service(1: string service_name,
                                 2: i32 port,
                                 3: bool is_lvs)
        throws(1: EThriftException.ncTException exp),

    /**
     * 移除应用服务
     * @param string service 服务名
     */
    void del_application_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取指定节点服务状态: systemctl status service_name
     * @param <string> node_uuid 节点uuid
     * @param <string> service_name 服务名
     */
    ECMSAgent.ncTServiceStatus get_service_status(1: string node_uuid,
                                                  2: string service_name)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 单点应用

    /**
     * 检查单点应用是否在集群中注册安装
     * @param   string  app_name    单点应用名称
     * @return  bool                True, 单点应用已在集群中安装
     *                              False, 单点应用未在集群中安装
     */
     bool is_app_registered(1: string app_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置单点应用节点
     * @param string node_uuid 节点uuid
     * @param string app_name
     */
    void add_single_application_node(1: string node_uuid,
                                     2: string app_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 取消单点应用节点
     * @param string app_name
     */
    void del_single_application_node(1: string app_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 根据节点获取单点应用服务
     * @param   string  node_uuid    节点 UUID
     * @return  list<ncTAPPServiceInfo>
     */
    list<ncTAppServiceInfo> get_single_application_service_by_node(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 根据应用获取单点应用节点UUID
     * @param   string  app_name    应用名
     * @return  string              节点 UUID
     */
    string get_node_uuid_by_app_name(1: string app_name)
        throws(1: EThriftException.ncTException ex),

    /**
     * 获取安装单点应用的节点 IP
     * @param   string  app_name    单点应用名称
     * @return  string              节点IP
     */
     string get_app_host_ip(1: string app_name)
        throws(1: EThriftException.ncTException exp),


    /////////////////////////////////////////////////////////////////
    // 10、登陆管理
    /////////////////////////////////////////////////////////////////

    /**
     * 验证登录信息
     * @param <string> user 用户名
     * @param <string> password 密码
     * @return 验证结果  uuid 验证通过
     *                   ncTSignRet.USER_ERR 用户名错误
     *                   ncTSignRet.PWD_ERR 密码验证失败
     */
     string verify_sign_in(1: string user,
                           2: string password)
        throws(1: EThriftException.ncTException exp),

    /**
     * 应用子系统是否可用,如果可用登陆验证使用应用子系统的验证接口
     * 如果不可用,则使用集群验证接口
     * @return True: 应用子系统可用
     *         False: 没有应用子系统,或应用子系统不可用
     */
    bool app_sys_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 修改密码
     * @param uuid 管理员用户uuid, 同ShareMgnt.NCT_USER_ADMIN
     * @param password 密码
     */
     void update_password(1: string uuid,
                          2: string password)
        throws(1: EThriftException.ncTException exp),

    /**
     * 修改用户名
     * @param uuid 管理员用户uuid, 同ShareMgnt.NCT_USER_ADMIN
     * @param user_name 用户名
     */
     void update_user_name(1: string uuid,
                           2: string user_name)
        throws(1: EThriftException.ncTException exp),


    /////////////////////////////////////////////////////////////////
    // 11、分布式配置管理
    // 用于向集群提交需要进行自动一致性管理的配置文件
    /////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////
    // 用于向集群提交需要进行自动一致性管理的配置文件

    /**
     * 提交配置文件，给集群进行自动一致性管理
     * 注意：提交后，所有节点将在检测周期内生效，不是立即生效。
     * @param string conf_file_path: 需在各节点保持一致的配置文件路径，
     *                               注意:需在AnyShareConfig/distributed_conf_files.conf中登记使配置
     *                               生效的回调命令，若未登记则不允许提交。
     * @param string source_file_path: 配置内容的来源文件路径，
     *                                 注意：若已在集群中提交过的配置文件，需再次提交时，最好不要在
     *                                 conf_file_path上直接进行修改然后作为来源文件提交，因为有可能
     *                                 会被集群自动还原。
     */
     void commit_conf_file(1: string conf_file_path, 2: string source_file_path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 提交配置文件内容，给集群进行自动一致性管理
     * 注意：提交后，所有节点将在检测周期内生效，不是立即生效。
     * @param string conf_file_path: 需在各节点保持一致的配置文件路径，
     *                               注意:需在AnyShareConfig/distributed_conf_files.conf中登记使配置
     *                               生效的回调命令，若未登记则不允许提交。
     * @param string file_content: 配置内容的来源文件内容。
     */
     void commit_conf_file_content(1: string conf_file_path, 2: string file_content)
        throws(1: EThriftException.ncTException exp),

    /**
     * 从集群中移除对指定配置文件的自动一致性管理
     * 若已移除，则忽略
     * @param string conf_file_path: 配置文件路径
     */
     void delete_conf_file(1: string conf_file_path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取已经提交到集群的分布式配置文件列表
     * @return map<string, ncTConfFileInfo>
     */
     map<string, ncTConfFileInfo> get_commited_conf_files()
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // DNS 配置 /etc/resolv.conf

    /**
     * 添加 DNS 服务器
     * @param nameservers: DNS 服务器地址列表，可以包含 0-3 个元素
     */
    void set_dns_server(1: list<string> nameservers)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取 DNS 服务器信息
     * @return DNS 服务器地址列表
     */
    list<string> get_dns_server()
        throws(1: EThriftException.ncTException exp),


    /////////////////////////////////////////////////////////////////
    // 12、外部时间源管理
    /////////////////////////////////////////////////////////////////

    /**
     * 获取时间同步服务状态
     * @return  bool    True:   启用
     *                  False:  禁用
     */
    bool get_chrony_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用时间同步服务
     **/
    void disable_chrony()
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用时间同步服务
     * 配置已添加的外部时间服务器
     */
    void enable_chrony()
        throws(1: EThriftException.ncTException exp),

    /**
     * 添加外部时间服务器, 可以是IP或域名, 若是域名则需要配置 dns
     * 限制，集群中存在离线节点时，不能添加外部时间服务器
     * @param string ntp_server: 外部时间服务器
     */
    void add_time_server(1: string server)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除指定外部时间服务器，不存在指定时间服务器仍可正常执行
     * @param string ntp_server: 外部时间服务器
     */
    void del_time_server(1: string server)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取当前集群中所有配置的外部时间服务器,不包含本地源 "127.127.1.0"
     */
    list<string> get_time_server()
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 13、服务模块化管理
    /////////////////////////////////////////////////////////////////

    /**
     * 安装服务
     * @param server_name 需要安装的服务名
     */
    void install_service(1: string server_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 卸载服务
     */
    void uninstall_service(1: string server_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取各个节点已安装的服务
     */
    list<ncTNodeServer> get_node_service()
        throws(1: EThriftException.ncTException exp),
}
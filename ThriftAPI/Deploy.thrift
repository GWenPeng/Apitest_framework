/*******************************************************************************************
DeployManager.thrift
    Copyright (c) Eisoo Software, Inc.(2013 - 2014), All rights reserved

Purpose:
        服务部署接口.

Author:
    ruan.yulin (ruan.yulin@eisoo.com)

Creating Time:
    2019-08-02
*******************************************************************************************/

include "EThriftException.thrift"
include "ECMSManager.thrift"

/**
 * 服务端口
 */
const i32 NCT_DEPLOYMANAGER_PORT = 9700
const i32 NCT_DEPLOYAGENT_PORT = 9701

// 服务信息
struct ncTServiceInfos {
    1: string service_name,
    2: string service_version,
    3: list<string> exception_nodes,
    4: list<string> installed_nodes,
}

// 安装包信息
struct ncTPackageInfo {
    1: string service_name,
    2: string package_name,
    3: string package_version,
    4: i64 upload_time,
    5: i64 package_size,
    6: string package_md5,
    7: string object_id,
    8: string oss_id,
}

// MongoDB 信息
struct ncTMongoDBInfo {
    1: list<string> hosts = [],
    2: i32 port = 0,
}


// 高可用类型
enum HaSys {
    NORMAL = 0,                         // 非高可用
    BASIC = 1,                          // 全局高可用
    APP = 2,                            // 应用高可用
    STORAGE = 3,                        // 存储高可用
    DB = 4,                             // 数据库高可用
}

// 高可用VIP信息
struct VipInfo {
    1: string ovip = '',                 // vip 地址
    2: string ivip = '',
    3: string mask = '',             // vip 子网掩码
    4: string nic = '',                 // vip 网卡
    5: i32 sys = HaSys.BASIC,     // 高可用类型
}

// 负载均衡类型
enum ncTLVSSys {
    APP = 1,                            // 应用负载均衡
    STORAGE = 2,                        // 存储负载均衡
}

// 高可用节点信息
struct HaNodeInfo {
    1: string node_uuid = '',           // 节点uuid
    2: string node_ip = '',             // 节点ip
    3: bool is_master = false,         // 是否高可用主
    4: i32 ha_sys = HaSys.NORMAL,     // 高可用类型
}

struct ReleaseInfo {
    1: string release_name = '',
}

struct CSNodeInfo {
    1: string cs_node_name = '',
    2: string node_uuid = '',
}

// 容器化服务信息
struct ContainerizedServiceInfo {
    1: string service_name = '',                // 服务名
    2: string available_version = '',           // 当前可更新版本
    3: string installed_version = '',           // 已安装版本
    4: list<string> nodes = [],                // 服务所在节点
    5: string available_package = '',            // 可用的安装包
    6: i32 replicas = 0,                        // 副本数
 }

// 容器化服务配置
struct ServiceConf {
    1: string service_name = '',
    2: list<string> node_ips = [],                   // 运行服务的节点ip列表
}

enum ncTDeployManagerError {
    NCT_NOT_APPLICATION_NODE = 50001,           // 当前节点不是应用节点
    NCT_SERVICE_PACKAGE_MISSING = 50002,        // 没有可用的安装包
    NCT_SERVICE_ALREADY_INSTALLED = 50003,      // 服务已安装
    NCT_SERVICE_NOT_INSTALL = 50004,            // 服务未安装
    NCT_SERVICE_VERSION_LOWER = 50005,          // 将要安装的版本低于已安装版本
    NCT_SERVICE_PACKAGE_DAMAGE = 50006,         // 安装包损坏

    NCT_NODE_IS_OFFLINE = 50007,                // 节点离线
    NCT_NODE_IS_MASTER = 50008,                // 当前节点为主节点，ERDS不可卸载
    NCT_NODE_TYPE_IS_INVALID = 50009,                // 参数无效
}

enum ncTVersionCheck {
    NCT_PACKAGE_VERSION_EQ_SERVICE_VERSION = 1,
    NCT_PACKAGE_VERSION_HIGER_THAN_SERVICE_VERSION = 2
}

/**
 * Manager接口
 */
service ncTDeployManager {
    /**
    * 上传安装包
    * @param package_path 安装包路径
    * throws   1、安装包损坏
    *          2、版本小于已安装版本
    */
    void deploy_upload_package(1: string package_path)
        throws(1: EThriftException.ncTException exp),

    /**
    * 删除安装包
    * @param service_name 服务名
    */
    void deploy_remove_package(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 获取服务信息
    * @param service_name 服务名
    * @return 返回服务信息
    */
    ncTServiceInfos deploy_get_service_infos(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 获取安装包信息
    * @param service_name 服务名
    * @return 返回安装包信息
    */
    ncTPackageInfo deploy_get_package_info(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 获取安装了某服务的所有节点uuid
    * @param service_name 服务名
    * return list<string> 节点ip列表
    */
    list<string> deploy_get_node_ip_by_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 安装服务
    * @param service_name 需要安装的服务
    * @param hosts 需要安装的节点
    * @return list<string> 安装失败的节点
    * @throws  1、非应用节点
    *          2、将要安装的版本低于当前版本
    *          3、需要安装的节点已安装服务
    *          4、升级低版本时需要升级的节点未安装服务
    *          5、没有可用的安装包
    *          6、节点离线
    */
    list<string> deploy_install_service(1: string service_name, 2: list<string> hosts)
        throws(1: EThriftException.ncTException exp),

    /**
    * 卸载服务
    * @param service_name 卸载的服务名
    * @param hosts 需要卸载的节点
    * @throws  1、未安装服务
    *          2、节点离线
    */
    void deploy_uninstall_service(1: string service_name, 2: list<string> hosts)
        throws(1: EThriftException.ncTException exp),

    /**
    * 根据节点获取已安装的服务
    * @param node_uuid 节点的uuid
    * return list<string> 服务名
    */
    list<string> deploy_get_services_by_node_ip(1: string ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 启动MongoDB
     */
    void deploy_start_MongoDB()
        throws(1: EThriftException.ncTException exp),

    /**
     * 安装 MongoDB
     * @param hosts 需要安装的节点，
     */
    void deploy_install_MongoDB(1: list<string> hosts)
        throws(1: EThriftException.ncTException exp),

    /**
     * 初始化 MongoDB 集群
     * @param uuids, MongoDB 集群 ip 列表, 必须 3 个节点才能初始化
     */
    void deploy_init_MongoDB_cluster(1: list<string> hosts)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取MongoDB节点ip
     * @return MongoDB信息，包括ip列表和端口
     */
    ncTMongoDBInfo deploy_get_MongoDB_infos()
        throws(1: EThriftException.ncTException exp),

    /**
     * 卸载 MongoDB， 只在初始化副本集之前可卸载
     * @param hosts, 需要卸载的节点
     */
    void deploy_uninstall_MongoDB(1: list<string> hosts)
        throws(1: EThriftException.ncTException exp),

    /**
     * 判断 MongoDB 是否可用
     */
    bool deploy_is_MongoDB_available()
        throws(1: EThriftException.ncTException exp),


    //***********************************************************
    // 高可用与负载均衡接口
    //***********************************************************
    /**
    * 设置高可用主节点
    * @param node_uuid 高可用主节点的uuid
    * @param vip_info 高可用VIP信息
    */
    void deploy_set_ha_master(1: string node_uuid, 2: VipInfo vip_info)
        throws(1: EThriftException.ncTException exp),

    /**
    * 设置高可用从节点
    * @param node_uuid 高可用从节点uuid
    * @param ha_sys 高可用类型
    */
    void deploy_set_ha_slave(1: string node_uuid, 2: HaSys ha_sys)
        throws(1: EThriftException.ncTException exp),

    /**
    * 取消高可用
    * @param node_uuid 节点uuid
    */
    void deploy_cancel_ha(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
    * 启用负载均衡
    * @param node_uuid 节点uuid
    * @param lvs_sys 负载均衡子系统
    */
    void deploy_enable_lvs(1: string node_uuid, 2: ncTLVSSys lvs_sys)
        throws(1: EThriftException.ncTException exp),

    /**
    * 停用负载均衡
    * @param node_uuid 节点uuid
    * @param lvs_sys 负载均衡子系统
    */
    void deploy_disable_lvs(1: string node_uuid, 2: ncTLVSSys lvs_sys)
        throws(1: EThriftException.ncTException exp),

    /**
    * 获取vip信息
    * @return list<VipInfo> vip信息列表
    */
    list<VipInfo> deploy_get_vip_info()
        throws(1: EThriftException.ncTException exp),

    /**
    * 设置vip
    * @param vip_info VIP信息
    */
    void deploy_set_vip_info(1: VipInfo vip_info)
        throws(1: EThriftException.ncTException exp),

    /**
    * 获取高可用节点信息
    * @return list<HaNodeInfo> 高可用节点信息列表
    */
    list<HaNodeInfo> deploy_get_ha_node_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 启用slb
     */
    void deploy_enable_slb()
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用slb
     * @throws: 集群内存在高可用
     */
    void deploy_disable_slb()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取slb是否启用
     */
    bool deploy_get_slb_status()
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除节点
     */
    void deploy_remove_node(1: ECMSManager.ncTNodeInfo node_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 节点进入主
     */
    void deploy_node_enter_master()
        throws(1: EThriftException.ncTException exp),

    /**
     * 节点进入从
     */
    void deploy_node_enter_slave()
        throws(1: EThriftException.ncTException exp),

    /**
     * slb 修复
     */
    void deploy_consistency_repair()
        throws(1: EThriftException.ncTException exp),

    /**
     * slb 修复
     */
    bool deploy_consistency_check()
        throws(1: EThriftException.ncTException exp),

    /**
     * cs集群初始化
     */
    void deploy_cs_init(1: map<string, string> data)
        throws(1: EThriftException.ncTException exp),

    /**
     * cs 添加节点
     */
    void deploy_cs_node_add(1: string ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 建立集群中所以机器互信
     */
    void deploy_machine_trust()
        throws(1: EThriftException.ncTException exp),

    /**
     * cs 删除节点
     */
    void deploy_cs_node_delete(1: string ip)
        throws(1: EThriftException.ncTException exp),

    /*
    * 设置节点角色
    * @param node_uuid 需要设置角色的节点
    * @param node_role 角色名
    * @throws  1、Proton_CS打标签失败
    *          2、数据库操作失败
    *          3、节点不属于当前集群
    *          4、角色名不合法
    *          5、可用的授权节点数不足
    */
    void deploy_set_node_role(1: string node_uuid, 2: string node_role)
        throws(1: EThriftException.ncTException exp),

    /*
    * 取消节点角色
    * @param 需要设置角色的节点
    * @param node_role 角色名
    * @throws  1、Proton_CS打标签失败
    *          2、数据库操作失败
    *          3、节点不属于当前集群
    *          4、角色名不合法
    */
    void deploy_cancel_node_role(1: string node_uuid, 2: string node_role)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取节点所有角色
     * @param node_uuid 节点uuid
     * @throws  1、节点不属于当前集群
     * @return list<string> 角色名列表
     */
    list<string> deploy_get_roles_by_node_uuid(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取角色的所有节点
     * @param node_role 角色
     * @throws  1、角色名不合法
     * @return list<string> 节点uuid列表
     */
    list<string> deploy_get_nodes_by_role(1: string node_role)
        throws(1: EThriftException.ncTException exp),

    /**
    * 更新secret对象
    * @param cert_type 证书类型，目前支持app
    */
    void deploy_update_secret(1: string cert_type)
        throws(1: EThriftException.ncTException exp),

    /**
    * 安装容器化服务
    * @param service_name 服务名
    * @param service_conf 服务配置，目前支持服务副本数配置
    */
    void deploy_install_containerized_service(1: ServiceConf service_conf)
        throws(1: EThriftException.ncTException exp),

    /**
    * 卸载容器化服务
    * @param service_name 服务名
    */
    void deploy_uninstall_containerized_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 上传容器化服务资源
    * @param package_path 包路径
    */
    void deploy_upload_containerized_service_package(1: string service_name, 2: string package_path)
        throws(1: EThriftException.ncTException exp),
    /**
    * 删除容器化服务资源
    */
    void deploy_remove_containerized_service_package(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 更新容器化服务版本
    * @param service_name 服务名
    */
    void deploy_upgrade_containerized_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),


    /**
    * 更改服务配置，如pod数等
    * @param service_name 服务名
    * @param service_conf 服务配置，目前支持服务副本数
    */
    // void deploy_update_containerized_service(1: ServiceConf service_conf)
    //     throws(1: EThriftException.ncTException exp),

    /**
    * 获取容器化服务信息
    * @param service_name 服务名
    */
    ContainerizedServiceInfo deploy_get_containerized_service_info(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 判断服务使用已安装
    * @param service_name 服务名
    * @return bool 已安装返回True
    */
    bool deploy_had_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 添加服务节点
    * @param service_name 服务名
    * @param node_ip 需要添加的节点ip
    */
    void deploy_containerized_service_add_node(1: string service_name, 2: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
    * 移除服务节点
    * @param service_name 服务名
    * @param node_ip 需要移除的节点ip
    */
    void deploy_containerized_service_remove_node(1: string service_name, 2: string node_ip)
        throws(1: EThriftException.ncTException exp),

}

/**
 * agent接口
 */
service ncTDeployAgent {
    /**
    * 安装服务
    * @param service_name 需要安装的服务名
    */
    void install_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 卸载服务
    * @param service_name 卸载的服务名
    */
    void uninstall_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 安装 MongoDB
     */
    void install_MongoDB()
        throws(1: EThriftException.ncTException exp),

    /**
     * 创建mongodb副本集
     */
    void init_mongodb_repl(1: list<string> hosts)
        throws(1: EThriftException.ncTException exp),

    /**
     * 卸载 MongoDB， 只在初始化副本集之前可卸载
     * @param hosts, 需要卸载的节点
     */
    void uninstall_MongoDB()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取副本集主节点 ip
     */
    string get_Primary_node_ip()
        throws(1: EThriftException.ncTException exp),

    /**
    * 清理erds数据库信息
    */
    void erds_clear_node()
        throws(1: EThriftException.ncTException exp),

    /**
     * cs 环境重置
     */
    void cs_reset(1: string ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * cs集群初始化
     */
    void cs_init(1: map<string, string> data)
        throws(1: EThriftException.ncTException exp),

    /**
     * cs更新配置
     */
    void cs_update_config(1: map<string, string> data)
        throws(1: EThriftException.ncTException exp),

    /**
     * cs 删除节点
     */
    void cs_node_delete(1: string ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * cs 添加节点
     */
    void cs_node_add(1: string ip)
        throws(1: EThriftException.ncTException exp),

     /**
     * 安装CR
     */
    void install_cr()
        throws(1: EThriftException.ncTException exp),

    /**
     * 建立集群中所以机器互信
     */
    void machine_trust()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取机器rsa内容
     */
    string get_machine_rsa()
        throws(1: EThriftException.ncTException exp),

    /**
    * 安装chart
    */
    void install_micro_service(1: string micro_service_name, 2: ServiceConf service_conf, 3: i32 timeout)
        throws(1: EThriftException.ncTException exp),

    /**
    * 卸载chart
    */
    void uninstall_micro_service(1: string micro_service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新服务版本
     */
    void upgrade_micro_service(1: string micro_service_name, 2: ServiceConf service_conf, 3: string operation)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取微服务信息
     */
    map<string, string> get_micro_service_info(1: string micro_service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 回滚微服务
     */
    void rollback_micro_service(1: string micro_service_name, 2: string revision)
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新vm.max_map_count
     */
    void update_vm_max_map_count()
        throws(1: EThriftException.ncTException exp),

    /**
    * 获取机器码
    */
    string get_machine_code()
        throws(1: EThriftException.ncTException exp),

    /*
    * 设置节点角色
    * @param node_uuid 需要设置角色的节点
    * @param node_role 角色名
    * @throws   1、Proton_CS打标签失败
    *           2、数据库操作失败
    *           3、节点不属于当前集群
    *           4、角色名不合法
    *           5、可用的授权节点数不足
    */
    void set_node_role(1: string node_uuid, 2: string node_role)
        throws(1: EThriftException.ncTException exp),

    /*
    * 取消节点角色
    * @param 需要设置角色的节点
    * @param node_role 角色名
    * @throws   1、Proton_CS打标签失败
    *           2、数据库操作失败
    *           3、节点不属于当前集群
    *           4、角色名不合法
    */
    void cancel_node_role(1: string node_uuid, 2: string node_role)
        throws(1: EThriftException.ncTException exp),

    /**
    * 更新secret对象
    * @param secret_name secret名
    */
    void update_secret(1: string secret_name)
        throws(1: EThriftException.ncTException exp),

    /**
    * 创建secret对象
    * @param secret_name secret名
    * @param ns secret所在命名空间
    * @param secret_type secret类型，目前仅支持tls
    * @param cert_type 证书类型，目前支持app
    */
    void create_secret(1: string secret_name, 2: string ns, 3: string secret_type, 4: string cert_type)
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新主机服务访问配置文件
     */
    oneway void update_access_conf()

    /**
     * 更新release副本数
     */
    void set_release_replicas(1: string release, 2: i32 replicas)
    /**
     * 创建pv
     */
    void create_pv(1: list<string> nodes, 2: string micro_service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 准备pv挂载路径
     */
    void prepare_pv_path(1: string micro_service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除pv
     */
    void delete_pv(1: string pv_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除pvc
     */
    void delete_pvc(1: string micro_service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取节点上pod名
     */
    list<string> get_pod_name_by_node(1: string name_space, 2: string node_ip)
        throws(1: EThriftException.ncTException exp),
}

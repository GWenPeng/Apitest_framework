/*********************************************************************
ECMSUpgrade.thrift:
    爱数集群升级管理接口定义文件

Purpose:
    此接口为集群升级管理接口, 提供集群业务逻辑层对外接口。
    thrift生成的remote客户端工具，访问示例如下：
    python ncTECMSUpgrade-remote -h host:port interface param

    eg:
        python ncTECMSUpgrade-remote -h 192.168.100.100:9603 start_upgrade

Creating Time:
    2017-08-22
**********************************************************************/

include "EThriftException.thrift"


// 端口号
const i32 NCT_UPGRADE_MANAGER_PORT = 9203
const i32 NCT_UPGRADE_AGENT_PORT = 9204

/**
 * 升级包信息
 */
struct ncTUpgradePackageInfo {
    1:string package_version = "",       // 升级包版本
    2:string support_version = "",       // 支持升级的版本
    3:i64    import_time = 0,            // 升级包导入时间, unix 时间戳, 精确到毫秒
    4:string package_hash = "",          // 升级包文件的散列值
    5:string hash_algorithm = ""         // 散列算法
    6:string package_name = "",          // 升级包名称
    7:i64    package_size = 0,           // 升级包大小
    8:string package_oss_id = '',     // 对象存储id
}

/**
 * 节点升级状态
 */
struct ncTNodeUpgradeStatus {
    1:string node_uuid = "",             // 节点 UUID
    2:string status = "",                // 节点升级状态, 如 "", "going", "done"
    3:string comment = "",               // 升级进度详细描述
    4:list<string> errors = [],          // 升级过程中的错误信息
    5:i64    last_time = 0,              // 最近一次升级进度更新的时间, unix 时间戳, 精确到毫秒
    6:i64    start_time = 0,             // 升级开始时间, unix 时间戳, 精确到毫秒
    7:string old_version = "",           // 升级前版本
    8:string new_version = "",           // 升级后版本
}

/**
 * ECMSUpgradeManager thift 管理接口
 */
service ncTECMSUpgradeManager {

    //////////////////////////////////////////////////////////////////////////
    // 以下接口用于升级包管理

    /**
     * 导入升级包
     * @param   string  path
     */
    void import_package(1: string path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 查询升级包信息
     */
    ncTUpgradePackageInfo query_package()
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除已导入的升级包, 未导入升级包不抛错
     */
    void remove_package()
        throws(1: EThriftException.ncTException exp),

    /**
     * 集群开始并发升级
     */
    void start_upgrade()
        throws(1: EThriftException.ncTException exp),

    //////////////////////////////////////////////////////////////////////////
    // 以下接口用于升级状态管理

    /**
     * 清理化升级状态
     * @param   bool    force   升级过程中时是否强制清理升级状态
     */
    void clear_status(1: bool force)
        throws(1: EThriftException.ncTException exp),

    /**
     * 查询升级状态
     */
    list<ncTNodeUpgradeStatus> query_status()
        throws(1: EThriftException.ncTException exp),
}

/**
 * ECMSUpgradeAgent thrift 管理接口
 */
service ncTECMSUpgradeAgent {
    /**
     * 查询升级包信息
     * @param   string  path    升级包路径
     */
    ncTUpgradePackageInfo query_package(1: string path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 导入升级包
     * @param   string  path    升级包路径
     */
    string import_package(1: string path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除已导入的升级包, 未导入升级包不抛错
     */
    void remove_package()
        throws(1: EThriftException.ncTException exp),

    /**
     * 当前节点启动升级
     * @param   string  name        升级包名称
     */
    oneway void start_upgrade(1: string name)
}

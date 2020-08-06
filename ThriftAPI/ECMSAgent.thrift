/*********************************************************************
ECMSAgent.thrift:
    爱数集群管理代理接口定义文件

Purpose:
    此接口为集群配置管理代理接口, 提供集群模块化功能实现接口。
    thrift生成的remote客户端工具，访问示例如下：
    python ncTECMSAgent-remote -h host:port interface param

    eg:
        python ncTECMSAgent-remote -h 192.168.100.100:9602 reboot_node

Creating Time:
    2017-08-10
**********************************************************************/

include "EThriftException.thrift"


// 端口号
const i32 NCT_ECMSAGENT_PORT = 9202

/**
 * Chrony角色
 */
enum ncTChronyRole {
    UNKNOWN = 0,
    MASTER = 1,
    SLAVE = 2,
}

// 服务状态
enum ncTServiceStatus{
    SS_STOPPED = 0,                     // 服务已停止
    SS_STARTED = 1,                     // 服务已启动
    SS_OTHER = 2,                       // 其他，比如部分停止
}

// 第三方日志主机及接收规则
struct ncTLogHostInfo{
    1: string facility,                     //日志模块
    2: string severity,                     //日志等级
    3: string ip,                           //日志服务器IP地址
    4: i32 port,                            //日志服务器端口
    5: string protocol,                     //传输协议
}

/**
 * 数据库实例信息结构
 */
struct ncTDBInstInfo {
    1: string service_name,            // 实例服务名
    2: string data_dir,                // 实例数据目录
    3: string socket,                  // 实例socket文件
    4: i32 port,                       // 实例启动端口
    5: string pid_file,                // 实例pid文件
    6: string mysqld_bin_path,         // mysql bin文件
    7: string log_error,               // 日志文件
    8: string package_name,            // 软件包名
    9: map<string, string> option = {}    //数据库配置信息
}

/**
 * 第三方数据库连接信息
 */
struct ncTExternalDBInfo {
    1: string db_host = '',             // 第三方数据库地址
    2: i32 db_port = 0,                 // 第三方数据库端口
    3: string db_user = '',             // 第三方数据用户名
    4: string db_password = '',         // 第三方数据库密码
}

/**
 * SSH 信息
 */
struct ncTSSHInfo {
    1: string host = '',                // 主机地址
    2: i32 port = 0,                    // 连接端口
    3: string user = '',                // ssh 用户
    4: string password = '',            // ssh 密码
}

/**
 * keepalived->virtual_server->real_server_>TCP_CHECK 信息
 */
struct ncTTCPCheckInfo {
    1: string connect_port,        // TCP_CHECK 健康检查端口
    2: string connect_timeout,     // TCP_CHECK 检查无响应超时时间
    3: string nb_get_retry,        // TCP_CHECK 检查失败重试次数
    4: string delay_before_retry,  // TCP_CHECK 检查失败重试间隔时间
}
/**
 * keepalived virtual_server 中 real_server 信息
 */
struct ncTRealServerInfo {
    1: string real_ip,             // real_server 的真实IP地址
    2: string port,                // real_server 检查的服务端口
    3: string weight,              // 节点的权值,数字越大权值越高
    4: ncTTCPCheckInfo tcp_check,  // keepalived 健康检查方式,采用 TCP_CHECK,检查IP,端口
}

/**
 * keepalived.conf virtual_server 相关信息
 */
struct ncTVirtualServerInfo {
    1: string virtual_ip,                               // 外部访问的 vip 地址
    2: string port,                                     // 负载均衡的服务端口
    3: string delay_loop,                               // 健康检查时间间隔,单位是秒
    4: string lb_algo,                                  // 负载均衡调度算法
    5: string lb_kind,                                  // lvs 负载均衡机制 [DAT|DR|TUN]
    6: string protocol,                                 // 转发协议类型[TCP|UDP]
    7: list<ncTRealServerInfo> real_server,             // keepalived real server 信息
    8: bool exists = false,                             // keepalived.conf 中是否存在 virtual_server 配置
}

/**
 * keepalived.conf global_defs 相关信息
 */
struct ncTGlobalDefsInfo {
    1: list<string> notification_email,  // keepalived 报警邮件接收地址,可配置多个
    2: string notification_email_from,   // keepalived 报警邮件发送的源地址
    3: string smtp_server,               // 邮件的 smtp_server 地址
    4: string smtp_connect_timeout,      // 连接 smtp_server 的超时时间
    5: string router_id,                 // keepalived 服务器标识
    6: bool exists = false,              // keepalived.conf 中是否存在 global_defs 配置
}

/**
 * vip结构
 */
struct ncTVirtualIPAddressInfo{
    1: string ipaddr = "",
    2: string netmask = "",
    3: string nic_name = "",
    4: string virtual_nic_name = ""
}

/**
 * keepalived 配置结构体
 */
struct ncTVrrpInstanceInfo{
    1: string vrrp_instance_name = '',        // keepalived vrrp_instance 名称
    2: string state = '',                     // keepalived 角色,主节点为MASTER, 备节点为BACKUP
    3: string interface_name = '',            // 用于指定 HA 监测的网络接口
    4: i32 virtual_router_id = 0,             // 虚拟路由标识,同一实例下主备必须一致
    5: i32 priority = 0,                      // 节点优先级,同一实例下主节点必须高于备节点
    6: string advert_int = '',                // 主备之间同步检查的时间间隔,单位是秒
    7:string auth_type = '',                  // 节点间通信验证类型
    8:string auth_pass = '',                  // 节点间通信验证密码
    9:list<ncTVirtualIPAddressInfo> virtual_ipaddress, // keepalived 虚拟IP信息
    10:string unicast_src_ip = '',            // 单播本地IP
    11:string unicast_peer = '',              // 单播对端IP
    12:bool exists = false                    // keepalived.conf 中是否存在 vrrp_instance 配置
}

/**
 * etcd 配置结构体
 */
struct ncTEtcdConfigInfo{
    1: string name,                           // 实例名
    2: string ad_peer_urls,                   // 广播地址
    3: string listen_peer_urls,               // 服务端监听地址
    4: string listen_client_urls,             // 客服端监听
    5: string ad_client_urls,
    6: string cluster_token,                  // 集群id
    7: string cluster,                        // etcd集群节点
    8: string data_dir,                       // 实例目录
    9: string cluster_state,                  // 实例启动方式
}

/**
 * etcd 实例结构体
 */
struct ncTEtcdMemberInfo{
    1: string id,                             // etcd id
    2: string name,                           // etcd 实例名
    3: string peerurl,
    4: string clienturl,                      // 客户端地址
    5: string isLeader,                       // 主节点标记
}

/**
 * 协议地址信息
 */
struct ncTIfAddr {
    1: string nic_dev_name = "",        // 协议地址所在接口设备名，如 em1,bond0,bond0.32等
    2: string label = "",               // 协议地址的标签，如bond0:1中的‘1’，bond0:ivip中的‘ivip’
                                        // 建议不要超过4个字符
    3: string ipaddr = "",              // IP 地址
    4: string netmask = "",             // 子网掩码
    5: string gateway = "",             // 网关
}

/**
 * 网络接口设备信息
 * 包括物理网卡、绑定网卡、vlan网卡等
 */
struct ncTNic {
    1: string nic_dev_name = "",        // 设备名，如 em1,bond0,bond0.32等
    2: bool is_up = false,              // 设备状态是 UP or DOWN
    3: string state_info = "",          // 设备状态详情
    4: string hw_info = "",             // 设备物理硬件信息
    5: list<ncTIfAddr> ifaddrs = [],    // 该设备上的协议地址列表
}

// The swift device information in the ring
struct ncTSwiftDevice {
    // unique integer identifier amongst devices.
    1: i32 dev_id = -1,
    // integer indicating which region the device is in.
    2: i32 region = -1,
    // integer indicating which zone the device is in;
    // a given partition will not be assigned to multiple devices within
    // the same (region, zone) pair if there is any alternative.
    3: i32 zone = -1,
    // the ip address of the device.
    4: string ip = "",
    // the tcp port of the device.
    5: i32 port = -1,
    // the device’s name on disk (sdb1, for example).
    6: string dev_name = "",
    // a float of the relative weight of this device as compared to others;
    // this indicates how many partitions the builder will try to assign to this device.
    7: double weight = -1,
    // count of partitions in this device.
    8: i64 partition_count = -1,
    // percentage off the desired amount of partitions a given device wants.
    // For instance, if the device wants (based on its weight relative
    // to the sum of all the devices’ weights) 123 partitions and it has 124
    // partitions, the balance value would be
    // 83% (1 extra / 123 wanted * 100 for percentage).
    9: double balance = -1,
    // The capacity of the device.
    10: double capacity_gb = -1,
}

// The swift ring information
struct ncTSwiftRing {
    // number of partitions = 2**part_power
    1: i32 part_power = 0,
    // The number of replicas for each partition.
    2: i32 replicas = 0,
    // The minimum number of hours between partition changes.
    // The minimum number of hours before a partition can be reassigned.
    // It used to decide if a given partition can be moved again.
    // This restriction is to give the overall system enough time to settle
    // a partition to its new location before moving it to yet another location.
    // While no data would be lost if a partition is moved several times quickly,
    // it could make that data unreachable for a short period of time.
    // This should be set to at least the average full partition replication time.
    // Starting it at 24 hours and then lowering it to what the replicator reports
    // as the longest partition cycle is best.
    3: i32 min_part_hours = 0,
    // Number of partitions in the ring.
    4: i64 partition_count = 0,
    // Number of regions in the ring.
    5: i32 region_count = 0,
    // Number of zones in the ring.
    6: i32 zone_count = 0,
    // Number of devices in the ring.
    7: i32 device_count = 0,
    // The balance of the ring. The balance value is the highest percentage
    // off the desired amount of partitions a given device wants.
    // For instance, if the “worst” device wants (based on its weight relative
    // to the sum of all the devices’ weights) 123 partitions and it has 124
    // partitions, the balance value would be
    // 83% (1 extra / 123 wanted * 100 for percentage).
    8: double balance = 0,
    // The version number of the ring has builded.
    9: i32 build_version = 0,
    // The physical capacity of the pool.
    10: double physical_capacity_gb = 0,
    // The logical capacity of the pool, like physical_capacity_gb / replicas.
    11: double logical_capacity_gb = 0,
}

// RAID 物理磁盘设备信息
struct ncTRaidPDInfo {
    1: string pd_devid = "",        // 该设备唯一标识：由 PD-$(raid_controller_type)-$(adapter_id)-$(enclosure_id)-$(slot_id) 组成的字串值
                                    // 在硬 RAID 环境中 Enclosure Device 与 Slot 号唯一确定一个磁盘
    2: double capacity_gb = 0,      // 该物理磁盘的容量，单位 GB
    3: string ld_devid = "",        // 该物理磁盘所属的逻辑设备ID，若未属于任何逻辑设备，则为 ""
    4: string firmware_state = "",  // 该物理磁盘的 Firmware state, 如 "Online, Spun Up", "Unconfigured(good), Spun Up", "Rebuild", "Hotspare, Spun Up" 等等
    5: string foreign_state = "",   // 该物理磁盘的 Foreign State, 如 "Foreign", "None"
    6: string device_id = "",       // 该物理磁盘的 Device Id
    7: bool is_hotspare = false,    // 该物理磁盘是否热备盘
}

// RAID 逻辑设备信息
struct ncTRaidLDInfo {
    1: string ld_devid = "",        // 该设备唯一标识：由 LD-$(raid_controller_type)-$(adapter_id)-$(ld_target_id) 组成的字串值
    2: string disk_dev_path = "",   // 该 RAID 在系统中对应的设备路径，如 /dev/md0, /dev/sdb 等
    3: double capacity_gb = 0,      // 该 RAID 的容量，单位 GB
    4: string raid_level = "",      // RAID 级别，如 "0", "1", "5", "6", "00", "10", "50", "60" 等等
    5: list<string> pd_devid_list = [], // 组成该逻辑设备的物理磁盘的pd_devid列表
    6: string state = "",           // 该 RAID 的 State，如 Optimal, Degraded
    7: string disk_group = "",      // 该 RAID 的 DiskGroup 编号
}

// 数据卷设备信息
// 数据卷：在数据盘上创建的逻辑分区设备
struct ncTDataVolume {
    1: string vol_dev_path = "",    // 该数据卷在系统中的设备路径，如 /dev/sdb1 等
    2: string disk_dev_path = "",   // 该数据卷所属数据盘在系统中的设备路径，如 /dev/sdb
    3: double capacity_gb = 0,      // 数据卷容量大小，单位 GB
    4: string fs_type = "",         // 文件系统类型，如 xfs
    5: string mount_uuid = "",      // 该数据卷的挂载点标识，若未创建过挂载点标识，则为 ""
    6: string mount_path = "",      // 该数据卷在系统中的挂载路径，若当前未挂载，则为 ""
    7: double used_size_gb = -1,    // 已使用空间，单位 GB，若当前未挂载，则未知
}

// 数据盘设备信息
// 数据盘：用于存储用户数据的磁盘设备
struct ncTDataDisk {
    1: string disk_dev_path = "",           // 该数据盘在系统中的设备路径，如 /dev/sdb 等
    2: double capacity_gb = 0,              // 磁盘容量，单位 GB
    3: string disk_model = "",              // 设备型号：LSI, ATA-xxxx, ISCSI等等
    4: map<string, ncTDataVolume> volumes = {},  // 该磁盘上创建的逻辑分区设备列表(数据卷)
                                            // map<disk_dev_path, data_volume>
}

// 卷设备信息
// 缓存卷, 系统卷, sysvol卷使用此结构获取
struct ncTVolume {
    1: string vol_dev_path = "",    // 该缓存卷在系统中的设备路径，如 /dev/sdb1 等
    2: string disk_dev_path = "",   // 该缓存卷所属磁盘在系统中的设备路径，如 /dev/sdb
    3: double capacity_gb = 0,      // 缓存卷容量大小，单位 GB
    4: double used_size_gb = -1,    // 已使用空间，单位 GB，若当前未挂载，则未知
    5: string fs_type = "",         // 文件系统类型，如 xfs
    6: string mount_path = "",      // 该缓存卷在系统中的挂载点路径，若当前未挂载，则为 ""
    7: string disk_model = "",      // 设备型号：LSI, ATA-xxxx, ISCSI等等
}

/**
 * 导入规则
 */
struct ncTImportRule {
    1: bool create_missing = false,     // 不存在是否创建
    2: bool update_existing = false,    // 存在是否更新
    3: bool delete_missing = false,     // 不存在是否移除
}

/**
 * ECMSAgent thift 管理接口
 */
service ncTECMSAgent {

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // !以下接口为节点软件管理 -> SoftwareAgent
    /**
     * 安装指定软件
     */
    void yum_install(1: string name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 卸载指定软件
     */
    void yum_remove(1: string name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 判断软件是否存在
     */
    bool yum_exist(1: string name)
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口提供网络时间同步管理 -> ChronyAgent

    /**
     * 获取当前节点 chrony 角色
     *
     * @return ncTChronyRole: chrony角色
     */
    ncTChronyRole get_chrony_role()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置集群同步时间源
     */
    void set_chrony_server()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置节点为 chrony client, 从集群中的 server 节点同步时间
     *
     * @param string server_ip: 集群 master 节点ip
     */
    void set_chrony_client(1: string server_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 清理 chrony 配置文件
     */
    void clear_chrony_config()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取 chrony 与当前使用的时间源的时间差异
     * @return double   + 当前时间领先于时间源
     *                  - 当前时间落后于时间源
     */
    double get_chrony_diff_from_ref()
        throws(1: EThriftException.ncTException exp),

    /**
     * chrony 执行 makestep 立刻与当前使用的时间源同步
     */
    void chrony_makestep()
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口提供服务管理功能 -> ServiceAgent
    /**
     * 启动服务: systemctl start service_name
     */
    void start_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 停止服务: systemctl stop service_name
     */
    void stop_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 重启服务: systemctl restart service_name
     */
    void restart_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取服务状态: systemctl status service_name
     */
    ncTServiceStatus get_service_status(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 启动服务并等待确定其已启动: systemctl start service_name
     * @param service_name  服务名
     * @param timeout       单位：秒，等待超时时间，超时将抛出异常
     */
    void start_service_certainly(1: string service_name, 2: i32 timeout)
        throws(1: EThriftException.ncTException exp),

    /**
     * 停止服务并等待确定其已停止: systemctl stop service_name
     * @param service_name  服务名
     * @param timeout       单位：秒，等待超时时间，超时将抛出异常
     */
    void stop_service_certainly(1: string service_name, 2: i32 timeout)
        throws(1: EThriftException.ncTException exp),

    /**
     * 异步重启服务：systemctl restart service_name
     * 发起重启命令，不等结果
     */
    oneway void restart_service_async(1: string service_name)

    /**
     * 重载服务: systemctl reload service_name
     * @param service_name  服务名
     */
    void reload_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取服务 pid
     * 根据 unit 文件中 ExecStart 获取命令
     * ps -eo pid,cmd 过滤 pid
     * @param   string      服务名
     * @return  list<i32>   进程号
     */
    list<i32> get_service_pids(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 根据pid停止服务
     * @param pid 进程id
     * 注意:停止使用kill -15, 若不能停止则使用kill -9
     */
    void stop_service_by_pid(1: string pid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 查询服务开机启动状态
     * @param string service_name 服务名
     */
    bool is_enabled(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置服务开机自启动
     * @param string service_name 服务名
     */
    void enable_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用服务开机自启动
     * @param string service_name 服务名
     */
    void disable_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 重载所有修改过的配置文件
     */
    void systemctl_daemon_reload()
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // !以下接口mysql管理 -> MysqlAgent
    /**
     * 获取数据库信息
     */
    ncTDBInstInfo get_db_info(1: string inst)
        throws(1: EThriftException.ncTException exp),

    /**
     * 根据端口号获取数据库信息
     */
    ncTDBInstInfo get_db_info_by_port(1: i32 port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取所有数据库信息
     */
    list<ncTDBInstInfo> get_all_db_info()
        throws(1: EThriftException.ncTException exp),

    /**
     * 从配置文件中获取数据库实例
     *
     * @return list<string> 实例列表
     */
    list<string> get_db_include_inst()
        throws(1: EThriftException.ncTException exp),

    /**
     * 验证my.cnf中指定实例是否存在
     */
    bool exist_inst(1: string inst_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 添加指定实例的配置
     *
     * @param conf_dict  {'server-id': '1'}
     * @param db_info    数据库实例信息
     */
    void add_inst_conf(1: map<string, string> conf_dict,
                       2: ncTDBInstInfo db_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 移除指定实例的配置
     *
     * @param service_name  服务名
     */
    void remove_inst(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 创建实例目录
     *
     * @param data_dir      数据目录
     */
    void create_inst_dir(1: string data_dir)
        throws(1: EThriftException.ncTException exp),

    /**
     * 启动指定mysql实例
     */
    void start_mysql_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 停止指定mysql实例
     */
    void stop_mysql_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 重启指定mysql实例
     */
    void restart_mysql_service(1: string service_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 使用mysqladmin ping检查指定数据库使用能连通
     * param <string> host 数据库地址
     * param <int> port 数据库端口
     * param <string> user 数据库用户名
     * param <string> password 数据库密码
     */
    bool is_port_alive(1: string host,
                       2: i32 port,
                       3: string user,
                       4: string password)
        throws(1: EThriftException.ncTException exp),

    /**
     * 修改数据库初始密码
     */
    void change_init_pwd(1: string unix_socket)
        throws(1: EThriftException.ncTException exp),

    /**
     * 创建用户，为指定端口配置访问账户及权限
     */
    void create_users(1: i32 port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 安装半同步插件
     *
     * @param port          数据库端口
     */
    void install_semisync_plugin(1: i32 port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 配置半同步
     *
     * @param service_name  数据库服务名
     * @param server_id     数据库服务编号，如 1 or 2
     */
    void set_semi_sync(1: string service_name,
                       2: string server_id)
        throws(1: EThriftException.ncTException exp),

    /**
     * 跳过半同步错误
     *
     * @param service_name  实例名
     * @param error_number     错误数
     */
    void skip_slave_error(1: string service_name, 2: string error_number)
        throws(1: EThriftException.ncTException exp),

    /**
     * 从指定远端数据库中查询当前的主库状态
     *
     * @param remote_ip             远端数据库访问 IP
     * @param remote_port           远端数据库实例端口
     * @return map<string, string>  远端数据库的主库状态
     */
    map<string, string> get_master_status(1: string remote_ip,
                                          2: i32 remote_port)
        throws(1: EThriftException.ncTException exp),

    /**
     *从指定远端数据库中查询当前的从库状态
     * @param remote_ip             远端数据库访问 IP
     * @param remote_port           远端数据库实例端口
     * @return map<string, string>  远端数据库的从库状态
     */
    map<string, string> get_slave_status(1: string remote_ip,
                                         2: i32 remote_port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 初始化数据目录
     */
    void init_mysql_data_dir(1: string data_dir)
        throws(1: EThriftException.ncTException exp),

    /**
     * innoxtrabackup备份数据目录
     *
     * @param port        数据库端口
     * @param data_dir    数据目录
     * @param path        备份目录
     */
    void innoxtrabackup_db(1: i32 port,
                           2: string data_dir,
                           3: string path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 发送备份数据目录
     *
     * @param data_dir  数据目录
     * @param ssh_info  ssh连接信息
     */
    void send_db_file(1: string data_dir,
                      2: ncTSSHInfo ssh_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 移除备份目录
     */
    void remove_xtrabackup_dir(1: string data_dir)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取服务器id
     *
     * @param ip          数据库访问 IP
     * @param port        数据库实例端口
     * @return server_id  数据库实例的 server-id
     */
    i32 get_server_id(1: string ip,
                      2: i32 port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 恢复备份文件
     *
     * @param path        备份目录
     * @param data_dir    数据目录
     */
    void reback_file(1: string path,
                     2: string data_dir)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置从库半同步
     *
     * @param master_ip      半同步的主节点ip
     * @param slave_ip       半同步的从节点ip
     * @param db_info        数据库实例信息
     */
    void set_semisync_on_slave_node(1: string master_ip,
                                    2: string slave_ip,
                                    3: ncTDBInstInfo db_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置主库半同步
     *
     * @param master_ip      半同步的主节点ip
     * @param slave_ip       半同步的从节点ip
     * @param db_info        数据库实例信息
     */
    void set_semisync_on_master_node(1: string master_ip,
                                     2: string slave_ip,
                                     3: ncTDBInstInfo db_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 开始半同步
     *
     * @param remote_master_dict    半同步的主信息
     * @param remote_slave_dict     半同步的从信息
     */
    void start_semisync(1: map<string, string> remote_master_dict,
                        2: map<string, string> remote_slave_dict)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置数据库模式
     *
     * @param ip             数据库 ip
     * @param port           数据库端口
     * @param is_read_only   True(只读模式), False(默认可读可写模式)
     */
    void set_db_mode(1: string ip,
                     2: i32 port,
                     3: bool is_read_only)
        throws(1: EThriftException.ncTException exp),

    /**
     * 导出数据库数据到指定目录
     *
     * @param ip            数据库 ip
     * @param port          数据库端口
     * @param db_list       需要导出的数据库
     * @param path          导出路径
     */
    map<string, string> dump_db_to_path(1: string ip,
                                        2: i32 port,
                                        3: list<string> db_list,
                                        4: string path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 导入数据库数据
     *
     * @param sql_path_dict  sql 文件路径
     * @param port           数据库端口
     */
    void import_sql_to_db(1: map<string, string> sql_path_dict,
                          2: i32 port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 连接指定节点的数据库,锁表或解锁
     *
     * @param ip            数据库 ip
     * @param port          数据库端口
     * @param lock_status   操作状态, True(锁表) False(解锁)
     */
    void lock_tables(1: string ip,
                     2: i32 port,
                     3: bool lock_status)
        throws(1: EThriftException.ncTException exp),

    /**
     * 清理指定数据库半同步
     *
     * @param ip            数据库 ip
     * @param port          数据库端口
     */
    void reset_db_semisync(1: string ip,
                           2: i32 port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 清除指定数据库节点 binlog_file_name 以前的所有二进制日志文件
     * @param ip            binlog文件
     * @param port          数据库端口
     */
    void del_binary_log_to_file(1: string binlog_file_name,
                                2: i32 db_port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取数据库名
     *
     * @param ip            数据库ip
     * @param port          数据库端口
     * @return list<string> db_list 数据库名列表
     */
    list<string> get_custom_databases(1: string ip,
                                      2: i32 port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 创建数据库
     *
     * @param database_list 需要创建的数据库名称列表
     * @param ip            数据库 ip
     * @param port          数据库端口
     */
    void create_database(1: list<string> database_list,
                         2: string ip,
                         3: i32 port)
        throws(1: EThriftException.ncTException exp),

    /*
     * 指定数据库创建test表，插入数据，删除test表
     */
    void make_instance_not_empty(1: string database,
                                 2: string ip,
                                 3: i32 port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 从数据库配置文件获取实例名
     *
     * @return list<string> 实例名列表
     */
    list<string> get_inst_from_conf()
        throws(1: EThriftException.ncTException exp),

    /**
     * 通过实例名获取实例配置
     *
     * @param string name   实例名
     * @return list<string> 实例配置
     */
    map<string, string> get_conf_by_inst_name(1: string name)
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // !以下接口为防火墙管理 -> FirewallAgent
    /*
     * 向指定区域添加rich规则
     * @param list<string> rich_rule_list 防火墙rich规则列表
     * @param string 规则目标区域
     * @param bool 是否为永久规则
     * 注意: 永久规则不立即生效,需要调用reload
     */
    void add_rich_rule(1: list<string> rich_rule_list,
                       2: string zone,
                       3: bool is_permanent)
        throws(1: EThriftException.ncTException exp),

    /*
     * 移除指定区域的rich规则
     * @param list<string> rich_rule_list 待移除防火墙rich规则列表
     * @param string 规则目标区域
     * @param bool 是否为永久规则
     * 注意: 永久规则不立即生效,需要调用reload
     */
    void remove_rich_rule(1: list<string> rich_rule_list,
                          2: string zone,
                          3: bool is_permanent)
        throws(1: EThriftException.ncTException exp),

    /*
     * 添加源地址到指定区域
     */
    void add_source(1: string source,
                    2: string zone,
                    3: bool is_permanent)
        throws(1: EThriftException.ncTException exp),

    /*
     * 从指定区域移除源地址
     */
    void remove_source(1: string source,
                       2: string zone,
                       3: bool is_permanent)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取指定区域防火墙信息:
     * @param option: 'rich-rule' 获取所有复杂规则 |
     *                'service'   获取服务 |
     *                'source'    获取源地址
     * @param zone: 防火墙区域
     * @param is_permanent: 是否获取永久规则
     */
    list<string> get_firewall_info(1: string option,
                                   2: string zone,
                                   3: bool is_permanent)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取指定区域的链规则
     */
    string get_target(1: string zone)
        throws(1: EThriftException.ncTException exp),

    /*
     * 设置指定区域的链规则
     * @param option: 'DEFAULT' | 'ACCEPT'
     */
    void set_target(1: string option,
                    2: string zone)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取防火墙默认区域
     */
    string get_default_zone()
        throws(1: EThriftException.ncTException exp),

    /*
     * 设置防火墙默认区域
     */
    void set_default_zone(1: string zone)
        throws(1: EThriftException.ncTException exp),

    /*
     * 移除服务
     */
    void remove_service(1: string service_name,
                        2: string zone,
                        3: bool is_permanent)
        throws(1: EThriftException.ncTException exp),

    /*
     * 重载防火墙
     * @param is_complete True:完全重载,相当于重启服务
                          False: 重载
     */
    void reload_firewall(1: bool is_complete)
        throws(1: EThriftException.ncTException exp),

    /*
     * 初始化成默认防火墙规则,仅允许22端口连接
     */
    void init_firewall_xml()
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // !以下接口为高可用管理 -> KeepalivedAgent
    /*
     * 设置高可用配置文件global区域
     */
    void set_global(1: string router_id)
        throws(1: EThriftException.ncTException exp),

    /*
     * 设置vrrp部分
     */
    void set_keepalived(1: ncTVrrpInstanceInfo vrrp_instance_info)
        throws(1: EThriftException.ncTException exp),

    /*
     * 设置lvs部分
     */
    void set_lvs(1: string virtual_ip,
                 2: list<i32> port_list,
                 3: list<string> real_ip_list)
        throws(1: EThriftException.ncTException exp),

    /*
     * 清理keepalived配置文件
     */
    void clear_keepalived()
        throws(1: EThriftException.ncTException exp),

    /*
     * 判断keepalived配置文件是否为空
     */
    bool keepalived_conf_is_empty()
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取 vrrp_instance 相关配置信息
     */
    ncTGlobalDefsInfo get_global_info()
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取 vrrp_instance 相关配置信息
     */
    list<ncTVrrpInstanceInfo> get_keepalived_info()
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取 lvs 相关配置信息
     */
    list<ncTVirtualServerInfo> get_lvs_info()
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取 lvs 端口
     */
    list<i32> get_lvs_port()
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取 lvs 对应端口的连接数
     * @param   string  host    虚拟主机地址
     * @param   int     port    端口号
     * @return  int             ipvsadm -ln 获取的指定端口的 ActiveConn 值
     */
    i32 get_lvs_active_conn(1: string host, 2: i32 port)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取 keepalived.conf real ip
     */
    list<string> get_real_ips()
        throws(1: EThriftException.ncTException exp),

    /*
     * 删除 vrrp_instance 相关配置
     */
    void del_keepalived_by_name(1: string inst_name,
                                2: bool need_reload)
        throws(1: EThriftException.ncTException exp),
    /*
     * 删除 lvs 配置
     */
    void del_lvs(1: bool need_reload)
        throws(1: EThriftException.ncTException exp),

    /*
     * 启动keepalived服务
     */
    void start_keepalived_service()
        throws(1: EThriftException.ncTException exp),

    /*
     * 停止keepalived服务
     */
    void stop_keepalived_service()
        throws(1: EThriftException.ncTException exp),

    /*
     * 重载keepalived服务
     * @param bool is_vrrp_changed vip是否改变
     */
    void reload_keepalived_service(1: bool is_vrrp_changed)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // !以下接口为etcd管理 -> EtcdAgent
    /*
     * 获取添加etcd时,etcd集群信息
     */
    string get_add_etcd_info(1: string cmd_str)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取etcd集群 member
     */
    list<ncTEtcdMemberInfo> get_etcd_member_list()
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取etcd服务pid
     * @param is_second: True 主节点上备用实例| False 普通实例
     */
    list<string> get_etcd_pid_list(1: bool is_second)
        throws(1: EThriftException.ncTException exp),

    /*
     * 向etcd集群添加一个实例
     * @param etcdinfo 启动实例的参数结构
     */
    void add_etcd_inst(1: ncTEtcdConfigInfo etcdinfo)
        throws(1: EThriftException.ncTException exp),

    /*
     * 从etcd集群移除一个实例
     * @param etcdid etcd实例id
     */
    void remove_etcd_inst(1: string etcdid)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取指定节点上的etcd实例状态,不包括主节点备实例
     */
    bool get_etcd_process_status()
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取etcd备实例状态
     */
    bool get_etcd_process_status_second()
        throws(1: EThriftException.ncTException exp),

    /*
     * 根据etcd结构启动etcd实例
     */
    void start_etcd_on_node(1: ncTEtcdConfigInfo etcdinfo)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取etcd数据目录路径列表
     */
    list<string> get_etcd_data_dir()
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取etcd健康信息
     */
    map<string, string> get_etcd_health_info()
        throws(1: EThriftException.ncTException exp),

    /*
     * 备份etcd数据目录到当前目录
     */
    void backup_etcd_data(1: string dir_path)
        throws(1: EThriftException.ncTException exp),

    /*
     * 发送etcd备份目录到指定节点指定目录下
     */
    void send_etcd_data(1: string data_dir,
                        2: map<string, string> ssh_dict)
        throws(1: EThriftException.ncTException exp),

    /*
     * 更新etcd peerurl地址
     */
    void update_etcd_peerurl(1: string member_id,
                             2: string url_str)
        throws(1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // !以下接口为系统管理 -> SysAgent

    /*
     * 获取指定目录的大小(单位:B)
     * @return int
     */
    i64 get_dir_size(1: string data_dir)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取指定目录的文件系统剩余空间(单位:B)
     * @return int
     */
    i64 get_fs_free(1: string mount_path)
        throws(1: EThriftException.ncTException exp),

    /*
     * 移动文件
     */
    void mv_dir(1: string src, 2: string desc)
        throws(1: EThriftException.ncTException exp),

    /*
     * 拷贝文件/目录：cp -r src desc
     */
    void cp_file(1: string src, 2: string desc)
        throws(1: EThriftException.ncTException exp),

    /*
     * 获取指定目录的文件
     */
    list<string> list_dir(1: string path)
        throws(1: EThriftException.ncTException exp),

    /*
     * 指定路径的文件/目录是否存在
     */
    bool exists_path(1: string path)
        throws(1: EThriftException.ncTException exp),

    /*
     * 删除指定目录
     */
    void rm_dir(1: string path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置集群配置文件
     * @param   string  db_host     数据库主机
     * @param   i32     db_port     数据库端口
     */
    void set_cluster_conf(1: string db_host, 2: i32 db_port)
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新集群数据库地址
     * @param   string  ipaddr ip地址
     */
    void update_cluster_ipaddr(1: string ipaddr)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取集群数据库地址
     */
    string get_cluster_ipaddr()
        throws(1: EThriftException.ncTException exp),

    /**
    * 创建节点磁盘配置文件(disk.conf)，并初始化
    * 若已存在则抛异常
    */
    void create_disk_conf()
        throws(1: EThriftException.ncTException exp),

    /**
    * 删除节点磁盘配置文件(disk.conf)
    */
    void remove_disk_conf()
        throws(1: EThriftException.ncTException exp),

    /**
    * 查询节点磁盘配置文件(disk.conf)是否存在
    */
    bool exists_disk_conf()
        throws(1: EThriftException.ncTException exp),

    /**
    * 查询节点磁盘配置文件(disk.conf)是否存在
    */
    string get_mount_extend_args()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置nsqlookupd地址
     */
    void set_nsqlookupd_addr(1: string ipaddr)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置nsqlookupd端口
     */
    void set_nsqlookupd_port(1: i32 port,
                             2: string connect_type)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取集群数据库地址
     */
    string get_nsqlookupd_addr()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置应用主节点 UUID
     * 缓存, 用于判断应用主节点是否发生切换
     */
    void set_app_master_node_uuid(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取应用主节点 UUID
     * 缓存, 用于判断应用主节点是否发生切换
     */
    string get_app_master_node_uuid()
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除集群配置文件(cluster.conf)
     */
    void remove_cluster_conf()
        throws(1: EThriftException.ncTException exp),

    /**
     * 查询集群配置文件(cluster.conf)是否已存在
     *
     * @return True 若已存在，False 若不存在
     */
    bool exists_cluster_conf()
        throws(1: EThriftException.ncTException exp),

    /**
     * 创建集群节点配置文件(nodeinfo.conf)，并初始化
     * 若已存在,则抛出异常
     *
     @param node_uuid(str):   集群节点uuid
     */
    void create_node_info_conf(1: string node_uuid)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除集群节点配置文件(nodeinfo.conf)
     */
    void remove_node_info_conf()
        throws(1: EThriftException.ncTException exp),

    /**
     * 查询集群节点配置文件(nodeinfo.conf)是否已存在
     *
     * @return True 若已存在，False 若不存在
     */
    bool exists_node_info_conf()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取集群节点配置(nodeinfo.conf)中的 node_uuid
     */
    string get_node_uuid()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置备份配置文件
     * @param   i32     package_count
     * @param   string  backup_time
     */
    void set_backup_conf(1: i32 package_count, 2: string backup_time)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取操作系统版本
     * @return  string  CentOS Linux release 7.2.1511 (Core)
     *                  CentOS Linux release 7.5.1804 (Core)
     */
    string get_os_version()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取 AnyShare 版本
     * @return  string  AnyShare-Server-6.0.0-20180604-816
     */
    string get_as_version()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取系统时间
     */
    string get_time()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置系统时间
     * @param string time_str
     */
    void set_time(1: string time_str)
        throws(1: EThriftException.ncTException exp),

    /**
     * 集群节点重启
     */
    void reboot_node()
        throws(1: EThriftException.ncTException exp),

    /**
     * 集群节点关机
     */
    void shutdown_node()
        throws(1: EThriftException.ncTException exp),

    /**
     * 禁用 selinux
     */
    void disable_selinux()
        throws(1: EThriftException.ncTException exp),

    /**
     * 执行 syspatch
     */
    void syspatch()
        throws(1: EThriftException.ncTException exp),

    /**
     * 添加 crontab 任务
     * @param   i32     minute  [0, 59]
     * @param   i32     hour    [0, 23]
     * @param   string  command 命令
     */
    void add_cron_job(1: i32 minute, 2: i32 hour, 3: string command)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除 crontab 任务
     * @param   string  command 命令
     */
    void del_cron_job(1: string command)
        throws(1: EThriftException.ncTException exp),

    /**
     * 配置rsyslog.conf远程日志服务器地址和端口
     * @param <ncTLogHostInfo> 日志服务器信息结构
     */
    void set_rsyslog_server(1: ncTLogHostInfo log_host_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 清除rsyslog.conf远程日志服务器地址和端口的配置
     * @param <ncTLogHostInfo> 日志服务器信息结构
     */
    void remove_rsyslog_server(1: ncTLogHostInfo log_host_info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取rsyslog.conf配置文件中远程服务器地址和端口
     * @return list<ncTLogHostInfo> 日志主机结构列表
     */
    list<ncTLogHostInfo> get_rsyslog_server()
        throws(1: EThriftException.ncTException exp),

    /**
     * 判断是否为asu节点
     * @return    True:    asu节点
     *            False:   非asu节点
     */
    bool is_asu_node()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取语言配置
     * @return    string:    语言配置
     */
    string get_language()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取语言配置
     * @param string: 语言配置
     */
    void set_language(1:string langstr)
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置节点第三方数据库连接信息
     * @param ncTExternalDBInfo info 第三方数据库信息
     *        ncTExternalDBInfo.db_host:第三方数据库地址,
     *        ncTExternalDBInfo.db_port:第三方数据库端口,
     *        ncTExternalDBInfo.db_user:第三方数据库用户,
     *        ncTExternalDBInfo.db_password:第三方数据库密码
     */
    void set_external_db_conf(1: ncTExternalDBInfo info)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取第三方数据库连接信息
     * @return ncTExternalDBInfo info 第三方数据库信息,结构属性同上
     */
    ncTExternalDBInfo get_external_db_conf()
        throws(1: EThriftException.ncTException exp),

    // 分布式配置文件管理

    /**
     * 校验指定配置文件是否一致
     * 若指定配置文件不存在，则返回不一致
     *
     * @param string conf_file_path: 配置文件路径
     * @param string conf_file_md5: 配置文件md5校验值
     * @return bool: True 一致，False 不一致
     */
    bool is_conf_file_consistency(
        1: string conf_file_path,
        2: string conf_file_md5)
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新指定配置文件内容,
     * 并依据distributed_conf_files.conf中登记的回调命令使配置更新生效,
     * 若未登记该配置文件的回调命令，则视为无回调命令.
     *
     * @param string conf_file_path: 配置文件路径
     * @param binary conf_file_content: 配置文件内容
     * @param string conf_file_md5: 配置文件内容的md5校验值
     */
    void update_distributed_conf_file(
        1: string conf_file_path,
        2: binary conf_file_content,
        3: string conf_file_md5)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取已在distributed_conf_files.conf中登记的配置文件列表
     */
    list<string> get_registered_distributed_conf_files()
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口用于 ZABBIX 配置文件管理 -> ZabbixAgent

    /**
     * 更新 zabbix-agentd 配置文件
     * @param   string  hostname    主机名
     * @param   string  server      zabbix-server 地址
     */
    void update_zabbix_agentd_config(1: string hostname, 2: string server)
        throws(1: EThriftException.ncTException exp),

    /** 获取 zabbix-agentd 配置文件
     * @return  map<string, string>     zabbix-agentd 配置
     */
    map<string, string> query_zabbix_agentd_config()
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新 zabbix-server 配置文件
     * @param   string  dbhost      主机
     * @param   i32     dbport      端口
     * @param   string  dbname      数据库
     * @param   string  dbuser      用户名
     * @param   string  dbpassword  密码
     */
    void update_zabbix_server_config(
        1: string dbhost,
        2: i32 dbport,
        3: string dbname,
        4: string dbuser,
        5: string dbpassword,
        6: string listenip,
    )
        throws(1: EThriftException.ncTException exp),

    /** 获取 zabbix-server 配置文件
     * @return  map<string, string>     zabbix-server 配置
     */
    map<string, string> query_zabbix_server_config()
        throws(1: EThriftException.ncTException exp),

    /**
     * 更新 zabbix gui 配置文件
     * @param   string  server
     * @param   i32     port
     * @param   string  database
     * @param   string  user
     * @param   string  password
     */
    void update_zabbix_gui_config(
        1: string server,
        2: i32 port,
        3: string database,
        4: string user,
        5: string password,
        6: string zbx_server,
        7: i32 zbx_server_port,
    )
        throws(1: EThriftException.ncTException exp),

    /** 获取 zabbix gui 配置文件
     * @return  map<string, string>     zabbix gui 配置
     */
    map<string, string> query_zabbix_gui_config()
        throws(1: EThriftException.ncTException exp),

    /**
     * 导入 zabbix 配置
     * @param   string      path    配置文件路径
     */
    void import_zabbix_config(1: string path)
        throws(1: EThriftException.ncTException exp),

    /**
     * 导入 zabbix action
     * @param   string          path    配置文件路径
     * @param   ncTImportRule   rule    导入规则
     * @return  list<i32>               actionid 列表
     */
    list<i32> import_zabbix_action(1: string path, 2: ncTImportRule rule)
        throws(1: EThriftException.ncTException exp),

    /**
     * 修改 apache 配置文件
     * 不再监听默认的 80 端口
     * @param   i32     listen_port     zabbix web 所监听的端口
     */
    void patch_apache(1: i32 listen_port)
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口用于系统网络配置管理 -> NetAgent

    /**
     * 获取系统 ip list
     */
    list<string> get_ip_addrs()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取vip可用的网卡名
     */
    list<string> get_interface_name_for_vip()
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取网络接口设备信息
     */
    list<ncTNic> get_nics()
        throws(1: EThriftException.ncTException exp),

    /**
     * 根据标签获取协议地址信息
     */
    ncTIfAddr get_ifaddr(1: string label)
        throws(1: EThriftException.ncTException exp),

    /**
     * 获取当前系统中指定 IP 的协议地址信息
     */
    ncTIfAddr get_ifaddr_by_ipaddr(1: string ipaddr)
        throws(1: EThriftException.ncTException exp),

    /**
     * 在指定接口设备上配置协议地址(持久化的)
     * @param ncTIfAddr ifaddr:  协议地址配置
     */
    void set_ifaddr(1: ncTIfAddr ifaddr)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除指定标签的协议地址(持久化的)
     * @param string label:    协议地址的标签，如bond0:1中的‘1’，bond0:inner_vip中的‘inner_vip’
     */
    void del_ifaddr(1: string label)
        throws(1: EThriftException.ncTException exp),

    /**
     * 绑定网卡
     * @param list<string> 网卡名列表
     */
    void bind_nics(1: list<string> nic_name_list)
        throws(1: EThriftException.ncTException exp),

    /**
     * 解绑网卡
     * @param string 网卡名
     */
    void unbind_nic(1: string bond_dev_name)
        throws(1: EThriftException.ncTException exp),

    /**
     * 指定 ip 的 arp 缓存是否存在
     * @param ipaddr ip地址
     */
    bool exists_arp(1: string ipaddr)
        throws(1: EThriftException.ncTException exp),

    /**
     * 删除指定地址的arp
     * @param string 网卡名
     */
    void del_arp(1: string ipaddr)
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口用于 ssh 远程管理, 依赖 salt-ssh -> ssh_agent

    /**
     * salt-ssh roster 配置文件中添加指定主机信息
     * @param   <string>    ssh_ip              SSH ip
     * @param   <i32>       ssh_port            SSH 端口
     * @param   <string>    ssh_user            SSH 用户
     * @param   <string>    ssh_passwd          SSH 密码
     */
    void add_roster_conf(
        1: string ssh_ip,
        2: i32 ssh_port,
        3: string ssh_user,
        4: string ssh_passwd)
        throws(1: EThriftException.ncTException exp),

    /**
     * salt-ssh roster 配置文件中删除指定主机信息
     */
    void del_ssh_from_roster(1: string ssh_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 清理 roster 配置
     */
    void clear_roster_conf()
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口用于临时配置 ring.

    /**
     * Create a ring with 2^<part_power> partitions and <replicas>.
     *
     * @param part_power(i32)       Set the number of partitions = 2**part_power.
     *                              In practice, The number of the partitions set to 100 times
     *                              the number of disk will have a better shot.
     * @param replicas(i32)         Set the number of replicas for each partition.
     *                              General set to 3.
     */
    void create_ring (1: i32 part_power,
                      2: i32 replicas)
        throws (1: EThriftException.ncTException exp),

    /**
     * Add a device to the ring.
     *
     * Adds devices to the ring with the given information.
     * No partitions will be assigned to the new device until after calling 'rebalance()'.
     * This is so you can make multiple device changes and rebalance them all just once.
     *
     * @param region(i32)               Set integer indicating which region the device is in.
     * @param zone(i32)                 Set integer indicating which zone the device is in;
     *                                  a given partition will not be assigned to multiple
     *                                  devices within the same (region, zone) pair if there is
     *                                  any alternative.
     * @param ip(str)                   Set the ip address of the device.
     * @param dev_name(str)             Set the device’s name on disk (sdb1, for example).
     * @param dev_capacity_gb(double)   Give the disk's capacity. It will be used to calculate
     *                                  weight of the device. Unit is GB.
     * @return dev_id(i32)              Return the id of the device(dev_id).
     */
    i32 add_device (1: i32 region,
                    2: i32 zone,
                    3: string ip,
                    4: string dev_name,
                    5: double dev_capacity_gb)
        throws (1: EThriftException.ncTException exp),

    /**
     * Remove a device from the ring.
     *
     * Removes the device(s) from the ring. This should normally just be used for
     * a device that has failed. For a device you wish to decommission, it's best
     * to set its weight to 0, wait for it to drain all its data, then use this
     * remove command. This will not take effect until after running 'rebalance'.
     * This is so you can make multiple device changes and rebalance them all just
     * once.
     *
     * @param dev_id(i32)               Set the id of the device.
     * @return bool device_exists       若设备不存在，则返回False，否则返回True
     */
    bool remove_device (1: i32 dev_id)
        throws (1: EThriftException.ncTException exp),

    /**
     * Changes the replica count to the given <replicas>.
     * A rebalance is needed to make the change take effect.
     *
     * @param replicas(int)     The number of replicas for each partition.
     */
    void change_replicas (1:i32 replicas)
        throws (1: EThriftException.ncTException exp),

    /**
     * Resets the device's weight.
     *
     * No partitions will be reassigned to or from the device until after running 'rebalance'.
     * This is so you can make multiple device changes and rebalance them all just once.
     *
     * @param dev_id(i32)               Set the id of the device.
     * @param dev_capacity_gb(double)   Give the disk's capacity. It will be used to calculate
     *                                  weight of the device. Unit is GB.
     */
    void change_weight(1: i32 dev_id, 2: double dev_capacity_gb)

    /**
     * Rebalance the ring.
     * Attempts to rebalance the ring by reassigning partitions that haven't been
     * recently reassigned.
     *
     * This is the main work function of the builder, as it will assign
     * and reassign partitions to devices in the ring based on weights,
     * distinct zones, recent reassignments, etc.
     *
     * The process doesn’t always perfectly assign partitions (that’d take
     * a lot more analysis and therefore a lot more time – I had code that
     * did that before). Because of this, it keeps rebalancing until the device
     * skew (number of partitions a device wants compared to what it has)
     * gets below 1% or doesn’t change by more than 1% (only happens with ring
     * that can’t be balanced no matter what).
     *
     * @return balance(double)  rebalance之后的负载均衡率，越接近0表示越均衡, 越大表示越不均衡.
     *                          若当前没有设备，则将生成一个空的ring文件，并返回 0.
     *                          若rebalance未生成 ring 文件，则返回 -1.
     */
    i64 rebalance ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 修改指定设备的 dev_name
     */
    void change_dev_name (1:i32 dev_id, 2:string dev_name)
        throws (1: EThriftException.ncTException exp),

    /**
     * 修改指定设备的 IP
     */
    void change_ip (1:i32 dev_id, 2:string ip)
        throws (1: EThriftException.ncTException exp),

    /**
     * Just rewrites the distributable ring file. This is done automatically after
     * a successful rebalance, so really this is only useful after one or more
     * 'change_dev_name' or 'change_ip' calls when no rebalance is needed but you want to send out the
     * new device information.
     */
    void write_ring ()
        throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口用于持久化 ring 配置的查询和保存

    /**
     * 判断是否存在持久化ring配置
     */
    bool is_persistent_ring_exists ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 备份上述生成或更新的ring临时配置文件到持久化存储
     * 需要 builder 和 ring 文件均存在的情况下，才允许备份，否则抛错
     */
    void backup_ring ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 从持久化存储中恢复ring配置文件到临时配置目录，以供上述临时配置接口使用
     * 若持久化ring配置不存在，则抛错
     */
    void restore_ring ()
        throws (1: EThriftException.ncTException exp),

    /**
     * Get md5 of the persistent ring file.
     * 若持久化ring配置不存在，则抛错
     *
     * @return ring_md5(string)   不存在则返回 ""
     */
    string get_persistent_ring_md5 ()
        throws (1: EThriftException.ncTException exp),

    /**
     * Get information about the persistent ring.
     * 若持久化ring配置不存在，则抛错
     *
     * @return ring_info(ncTSwiftRing)
     */
    ncTSwiftRing get_persistent_ring_info ()
        throws (1: EThriftException.ncTException exp),

    /**
     * Get devices in the persistent ring.
     * 若持久化ring配置不存在，则抛错
     *
     * @return map<ncTSwiftDevice.dev_id, ncTSwiftDevice>
     */
    map<i32, ncTSwiftDevice> get_persistent_ring_devices ()
        throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口用于管理本机的 working ring.

    /**
     * 刷新本机swift服务所加载的ring文件，使最新的ring配置在本机生效。
     * 若持久化ring配置不存在，则抛错.
     * 若 ring 配置存在，但持久化ring文件为空则忽略.
     */
    void refresh_working_ring ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取本机swift服务所加载的ring文件的MD5校验值。
     *
     * @return md5(str)     ring 文件的md5校验值, 若ring文件不存在或为空，则返回 ""
     */
    string get_working_ring_md5 ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 清理本机swift服务所加载的ring文件，停止本机的swift服务。
     */
    void clear_working_ring ()
        throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口用于管理本机的 swift 服务.

    /**
     * 启动 swift 服务
     */
    void start_swift_service()
        throws(1: EThriftException.ncTException exp),

    /**
     * 停止 swift 服务
     */
    void stop_swift_service()
        throws(1: EThriftException.ncTException exp),

    /**
     * 重启 swift 服务
     */
    void restart_swift_service()
        throws(1: EThriftException.ncTException exp),

    /**
     * 查询 swift 服务是否启动
     */
    bool is_service_started()
        throws(1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // 以下接口用于查询存储池的健康情况.

    /**
     * 查询当前存储池的副本健康度.
     * 内部采用抽样的方法检测.
     * @return health_percent   返回健康百分比之分子，等于 100 可视为健康。
     *                          若持久化ring尚不存在，或者ring文件为空，则返回 -1
     */
    double get_replicas_health()
        throws (1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口提供raid管理
    // PS：RAID型号暂仅支持LSI

    /**
     * 查询连接到 RAID 卡上的物理磁盘设备列表
     *
     * @return pdlist(map<pd_devid, ncTRaidPDInfo>):    返回物理磁盘设备列表
     */
    map<string, ncTRaidPDInfo> get_raid_pdlist ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询指定 RAID 物理磁盘设备的详细信息
     *
     * @param string pd_devid:     设备唯一标识
     * @return map<key, value>:    RAID 物理磁盘设备的详细信息
     */
    map<string, string> get_raid_pd_details (1: string pd_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询数据 RAID 磁盘设备列表
     *
     * @return pdlist(map<pd_devid, ncTRaidPDInfo>):    返回物理磁盘设备列表
     */
    map<string, ncTRaidPDInfo> get_data_raid_pdlist ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询系统 RAID 磁盘设备列表
     *
     * @return pdlist(map<pd_devid, ncTRaidPDInfo>):    返回物理磁盘设备列表
     */
    map<string, ncTRaidPDInfo> get_sys_raid_pdlist ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询 RAID 卡上已创建的逻辑设备列表(即 RAID 列表)
     *
     * @return ldlist(map<ld_devid, ncTRaidLDInfo>):    返回逻辑设备列表
     */
    map<string, ncTRaidLDInfo> get_raid_ldlist ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询指定 RAID 逻辑设备的详细信息
     *
     * @param string ld_devid:     设备唯一标识
     * @return map<key, value>:    RAID 逻辑设备的详细信息
     */
    map<string, string> get_raid_ld_details (1: string ld_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询数据 RAID 列表
     *
     * @return ldlist(map<ld_devid, ncTRaidLDInfo>):    返回逻辑设备列表
     */
    map<string, ncTRaidLDInfo> get_data_raid_ldlist ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询系统 RAID 列表
     *
     * @return ldlist(map<ld_devid, ncTRaidLDInfo>):    返回逻辑设备列表
     */
    map<string, ncTRaidLDInfo> get_sys_raid_ldlist ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 清理指定数据 RAID 物理磁盘设备
     *
     * @param string pd_devid       物理磁盘唯一标识
     */
    void clear_data_raid_pd (1: string pd_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 检查指定的数据RAID物理磁盘状态是否good(可用于正常创建RAID)
     *
     * @param string pd_devid       物理磁盘唯一标识
     * @return bool                 good or not.
     */
    bool is_data_raid_pd_good (1: string pd_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 创建 RAID
     *
     * @param pd_devid_list(list<str>)  指定物理磁盘ID列表
     *                                  可由接口 get_raid_pdlist() 获取
     * @param raid_level(str)           RAID 级别，暂仅支持：["0", "1", "5"]
     * @return ld_devid(str)            返回所创建的逻辑设备ID
     */
    string create_raid (1: list<string> pd_devid_list,
                        2: string raid_level)
        throws (1: EThriftException.ncTException exp),

    /**
     * 删除 RAID
     *
     * @param ld_devid      指定逻辑设备ID，
     *                      可由接口 get_raid_ldlist()获取
     *                      或接口 create_raid()返回
     */
    void remove_raid (1: string ld_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 添加指定RAID的热备盘
     *
     * @param pd_devid      指定用作热备盘的物理磁盘设备ID
     * @param ld_devid      指定配置热备盘的逻辑设备ID，若为 "", 则设置为全局热备盘
     */
    void add_raid_hotspare (1: string pd_devid, 2: string ld_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 删除热备盘
     *
     * @param pd_devid      物理磁盘设备ID
     */
    void remove_raid_hotspare (1: string pd_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 将指定磁盘下线
     *
     * @param pd_devid      物理磁盘设备ID
     */
    void offline_raid_pd (1: string pd_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询 RAID 重建进度
     * 当PD设备的 fireware status 显示为 Rebuild 时，可通过该接口查询 Rebuild 的进度
     *
     * @param pd_devid      指定需要查询Rebuild进度的物理磁盘设备ID
     */
    string get_raid_rebuild_progress (1: string pd_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取raid型号,执行MegaCli -AdpAllInfo -aALL命令,获取Product Name的值
     * @return string raid型号
     */
    string get_raid_product_name ()
        throws (1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口提供数据盘和数据卷管理
    //
    //     数据盘：用于存储用户数据的磁盘设备, 包括直接连接到系统的物理磁盘，或RAID上创建的逻辑设备，
    // 或连接到系统的ISCSI设备等一切被OS正常驱动的存储设备。
    //     数据卷：在数据盘上创建的逻辑分区设备。
    //
    // 磁盘用途识别策略：
    // 缓存卷：卷标为 data-cache 的分区设备.
    // 系统盘：存在分区或lvm卷已挂载到 / 或 /sysvol，或存在缓存卷.
    // 其他盘：1. 系统盘之外，存在分区挂载到非 /sysvol/srv/node 路径，或存在lvm卷，或存在分区已用于lvm pv;
    //         2. Infoworks 特有的 zram0 内存挂载的系统启动盘.
    // 数据盘：系统盘及其他盘之外的磁盘.

    /**
    * 获取当前节点是否存在外挂存储
    * @return bool:  True存在，False不存在
    */
    bool exist_iscsi_device ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取指定磁盘信息
     * @param string dev_path 设备路径
     * @return map<string, string> 节点信息字典
     */
    map<string, string> get_disk_info (1: string dev_path)
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取系统卷信息
     * @return <ncTVolume>        返回系统卷结构
     */
    ncTVolume get_sys_volume ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取sysvol卷信息
     * @return <ncTVolume>        返回卷结构
     */
    ncTVolume get_sysvol_volume ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询数据盘列表
     *
     * @return data_disks(map<disk_dev_path, ncTDataDisk>)        返回数据盘列表
     */
    map<string, ncTDataDisk> get_data_disks ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询指定数据盘信息
     *
     * @param string disk_dev_path  指定数据盘路径
     * @return ncTDataDisk          返回数据盘信息
     */
    ncTDataDisk get_data_disk (1: string disk_dev_path)
        throws (1: EThriftException.ncTException exp),

    /**
     * 清理指定数据盘
     *
     * @param disk_dev_path(str)    指定数据盘在系统中的设备路径
     */
    void clear_data_disk (1: string disk_dev_path)
        throws (1: EThriftException.ncTException exp),

    /**
     * 检查当前节点的指定数据磁盘是否不干净
     * 干净标准：数据盘不存在分区
     *
     * @param disk_dev_path(str)    指定数据盘在系统中的设备路径
     * @return is_dirty(bool):      True 不干净，False 干净
     */
    bool is_data_disk_dirty (1: string disk_dev_path)
        throws (1: EThriftException.ncTException exp),

    /**
     * 查询指定数据卷信息
     *
     * @param string vol_dev_path   指定数据卷路径
     * @return ncTDataVolume        返回数据卷信息
     */
    ncTDataVolume get_data_volume (1: string vol_dev_path)
        throws (1: EThriftException.ncTException exp),

    /**
     * 在指定数据盘上创建数据卷
     *
     * @param disk_dev_path(str)    指定数据盘在系统中的设备路径
     * @param size_gb(float)        需要创建的数据卷大小
     * @return vol_dev_path(str)    返回所创建的数据卷设备路径
     */
    string create_data_volume (1: string disk_dev_path, 2: double size_gb)
        throws (1: EThriftException.ncTException exp),

    /**
     * 删除指定数据卷
     *
     * @param vol_dev_path(str)     指定数据卷在系统中的设备路径
     */
    void remove_data_volume (1: string vol_dev_path)
        throws (1: EThriftException.ncTException exp),

    /**
     * 挂载指定数据卷
     *
     * @param vol_dev_path  指定数据卷在系统中的设备路径
     */
    void mount_data_volume (1: string vol_dev_path)
        throws (1: EThriftException.ncTException exp),

    ///////////////////////////////////////////////////////////////////
    // 以下接口提供数据挂载点管理

    /**
     * 列举数据挂载点
     * @return list<string> mount_uuids  返回挂载点的UUID标识列表
     */
    list<string> get_data_mount_points ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 创建数据挂载点：
     *     创建挂载点目录，格式化指定数据卷，并增加指定数据卷的挂载点标识配置，并挂载
     *
     * @param mount_uuid    指定挂载点的UUID标识，挂载目录以该UUID命名，
     *                      且数据卷中将关联对应的UUID挂载标识，
     *                      用于在挂载时识别数据卷与挂载点的对应关系
     *                      PS：若为""，则自动生成一个新的UUID。
     * @param vol_dev_path  指定要关联该挂载点的数据卷路径
     * @return mount_uuid   返回挂载点标识
     */
    string create_data_mount_point (1: string mount_uuid, 2: string vol_dev_path)
        throws (1: EThriftException.ncTException exp),

    /**
     * 删除数据挂载点：
     *     卸载指定挂载点，并删除该挂载点目录
     * @param mount_uuid  指定挂载点的UUID标识
     */
    void remove_data_mount_point (1: string mount_uuid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 数据挂载点是否存在 Input/output error
     * @param       string      mount_uuid      挂载点 UUID
     * @return      bool                        True: 存在 IO error; False 不存在 IO error
     */
    bool exists_io_error(1: string mount_uuid)
        throws (1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口提供缓存卷管理
    //     缓存卷：label 为 data-cache

    /**
     * 在指定数据盘上创建缓存卷
     *
     * @param disk_dev_path(str)    指定数据盘在系统中的设备路径
     * @return vol_dev_path(str)    返回所创建的缓存卷设备路径
     */
    string create_cache_volume (1: string disk_dev_path)
        throws (1: EThriftException.ncTException exp),

    /**
     * 删除缓存卷
     */
    void remove_cache_volume ()
        throws (1: EThriftException.ncTException exp),


    /**
     * 获取缓存卷信息
     */
    ncTVolume get_cache_volume ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 初始化缓存卷
     * 若缓存卷存在，则：清除缓存卷及缓存目录中的数据，并挂载
     * 若缓存卷不存在，则：清除缓存目录中的数据
     */
    void init_cache_volume ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 判断缓存卷是否已初始化
     * 若缓存卷存在，若缓存卷中无数据，且已挂载，则已初始化
     * 若缓存卷不存在，若缓存目录存在，且无数据，则未初始化
     */
    bool is_cache_volume_inited ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 挂载缓存卷
     * 若缓存卷不存在，则忽略
     * 若缓存卷挂载失败，则记日志
     */
    void mount_cache_volume ()
        throws (1: EThriftException.ncTException exp),

    /**
     * 为各应用分配缓存卷
     */
    void allocate_cache_volume ()
        throws (1: EThriftException.ncTException exp),

    /////////////////////////////////////////////////////////////////
    // 以下接口为 zabbix 监控使用,包括SSD,Raid,Physical Disk,volume

    /**
     * 获取系统SSD设备列表
     * 如果不存在SSD,则返回为空列表如 []
     * 如果存在SSD,则返回SSD的磁盘名称如 ["/dev/sda", "/dev/sdb"]
     * 若存在SSD,但是在RAID中,则返回形式如 ["PD-LSI-0-6-12","PD-LSI-0-6-13"]
     *
     * @return list<string>: 返回SSD设备列表
     */
    list<string> get_ssd_disks()
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取系统SSD设备健康状态
     *
     * @param string: ssd 设备名称如 /dev/sda,如果在RAID中则名称为 PD-LSI-0-6-12
     * @return map<string, string>: 返回SSD设备创建状态
     */
    map<string, string> get_ssd_status(1: string device_name)
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取系统RAID列表
     * 列表中元素为 RAID 在系统中的唯一标识：
     * 由 LD-$(raid_controller_type)-$(adapter_id)-$(ld_target_id) 组成的字串值
     * 如 LD-LSI-0-0
     *
     * @return list<string>: RAID 标识的列表
     */
    list<string> get_raid_list()
        throws (1: EThriftException.ncTException exp),

    /**
     * 根据RAID的唯一标识,获取RAID状态信息
     * RAID 在系统中的唯一标识：
     * 由 LD-$(raid_controller_type)-$(adapter_id)-$(ld_target_id) 组成的字串值
     * 如 LD-LSI-0-0
     *
     * @return map<string, string>: RAID 状态信息
     */
    map<string, string> get_raid_status(1: string ld_devid)
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取RAID中 Physical Disk 的 pd_devid
     * 列表中元素为 pd_devid
     * 由 PD-$(raid_controller_type)-$(adapter_id)-$(enclosure_id)-$(slot_id) 组成的字串值
     * 如 PD-LSI-0-6-12
     *
     * @return list<string>: Physical Disk 标识的列表
     */
    list<string> get_physical_disk_list()
        throws (1: EThriftException.ncTException exp),

    /**
     * 根据Physical Disk的唯一标识,获取磁盘状态信息
     * Physical Disk 在系统中的唯一标识：
     * 由 PD-$(raid_controller_type)-$(adapter_id)-$(enclosure_id)-$(slot_id) 组成的字串值
     * 如 PD-LSI-0-6-12
     *
     * @return map<string, string>: physical_disk 状态信息
     */
    map<string, string> get_physical_disk_status(1: string pd_devid)
        throws (1: EThriftException.ncTException exp),

    ///////////////////////////////////////////////////////////////////////////
    // 以下接口管理外部时间源

    /**
     * 添加NTP源到本节点
     * 只有NTP主节点才能添加NTP源
     */
    void add_time_server(1: string server)
        throws (1: EThriftException.ncTException exp),

    /**
     * 从本节点中删除NTP源
     * 只有NTP主节点才能删除NTP源
     */
    void del_time_server(1:string server)
        throws (1: EThriftException.ncTException exp),

    ///////////////////////////////////////////////////////////////////////////
    // 以下接口提供nsq模块管理功能
    /**
     * 获取nsqlookupd服务绑定的端口
     * @param connect_type 访问方式 参数'tcp' 或 'http'
     * @return <int> 端口号
    **/
    i32 get_nsqlookupd_port(1:string connect_type)
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取nsqlookupd服务绑定的端口
     * @param addr_list 已经构造好的地址列表['127.0.0.1:4161']
    **/
    void set_nsqd_lookup_addrs(1:list<string> addr_list)
        throws (1: EThriftException.ncTException exp),

    /**
     * 获取nsqd注册地址
     * @return list<str> 已经构造好的地址列表['127.0.0.1:4161']
    **/
    list<string> get_nsqd_lookup_addrs()
        throws (1: EThriftException.ncTException exp),

    /**
     * 初始化nsqd缓存文件夹
     */
    void init_nsqd_cache_dir()
        throws(1: EThriftException.ncTException exp),

    /**
     * 判断是否存在nsqd缓存文件
     * @return <bool>
     */
    bool exists_nsqd_cache_file()
        throws(1: EThriftException.ncTException exp),

    /**
     * 设置nsqd配置的node_id
     */
    void set_nsqd_node_id(1: i32 node_id)
        throws(1: EThriftException.ncTException exp),
    
    /**
     * 设置nsqd配置的broadcast address
     */
    void set_nsqd_braodcast_address(1: string node_ip)
        throws(1: EThriftException.ncTException exp),

    /**
     * 是否安装有服务
     */
    list<string> installed_service(1: list<string> service_names)
        throws(1: EThriftException.ncTException exp),
}

import pulumi
from pulumi import ResourceOptions
from pulumi_gcp import compute
import init_scripts

#setup the network settings
network=compute.Network("network-4-demo")

firewall=compute.Firewall(
    "firewall-4-demo",
    network=network.self_link,
    allows=[
        compute.FirewallAllowArgs(
            protocol="tcp",
            ports=["22"]
        ),
        compute.FirewallAllowArgs(
            protocol="tcp",
            ports=["80"]
        )
    ]
)


#setup the policy server and init it with the script
instance_srvaddr=compute.Address("addr-4-demoserver",network_tier="STANDARD")
instance_srv=compute.Instance(
    "instance-4-policyserver",
    machine_type="e2-small",
    boot_disk=compute.InstanceBootDiskArgs(
        initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
            image="ubuntu-os-cloud/ubuntu-1804-bionic-v20200414"
        ),
    ),
    network_interfaces=[
        compute.InstanceNetworkInterfaceArgs(
            network=network.id,
            access_configs=[compute.InstanceNetworkInterfaceAccessConfigArgs(
                nat_ip=instance_srvaddr.address,
                network_tier="STANDARD"
            )]
        )
    ],
    metadata_startup_script=init_scripts.init_server,
    opts=ResourceOptions(delete_before_replace=True),
    zone="asia-east1-a",
)

#setup the client instance and setup the key
instance_clientaddr=compute.Address("addr-4-democlient",network_tier="STANDARD")
instance_client=compute.Instance(
    "instance-4-policyclient",
    machine_type="e2-small",
    boot_disk=compute.InstanceBootDiskArgs(
        initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
            image="ubuntu-os-cloud/ubuntu-1804-bionic-v20200414"
        ),
    ),
    network_interfaces=[
        compute.InstanceNetworkInterfaceArgs(
            network=network.id,
            access_configs=[compute.InstanceTemplateNetworkInterfaceAccessConfigArgs(
                nat_ip=instance_clientaddr.address,
                network_tier="STANDARD"
            )]
        )
    ],
    metadata_startup_script=init_scripts.init_client,
    metadata={"ssh-keys":"auditor:"+init_scripts.init_client_trusted_key},
    opts=ResourceOptions(delete_before_replace=True),
    zone="asia-east1-a",
)

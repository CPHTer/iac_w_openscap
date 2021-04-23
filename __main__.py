import pulumi
import infrabase


#export resources
pulumi.export("server instance_name",infrabase.instance_srv)
pulumi.export("server instance_external_ip", infrabase.instance_srvaddr.address)
pulumi.export("client instance_name",infrabase.instance_client)
pulumi.export("client instance_external_ip",infrabase.instance_clientaddr)
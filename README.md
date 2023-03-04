# NPA-G11-2023

Before do lab you should connect to "IT KMITL" vpn and make sure you have routing to 172.31.Y.0/24 to default vpn route
when enable feature not sand all traffic to vpn bacause when use enable this feature ip not connect in vpn routing for
private lab is not forwarding to default route vpn

if you enable not send all traffic to vpn please manually add route to forwarding packet to vpn

### Contributor

#### นายนพวรรณ ปักอินทรีย์ 63070092
#### นายภานุพงศ์ เฉลยรัตน์ 63070134

### Example

``` sudo route -n add -net 172.31.111.0/24 10.253.190.1 ```


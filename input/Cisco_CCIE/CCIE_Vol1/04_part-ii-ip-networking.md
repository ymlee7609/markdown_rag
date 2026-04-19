## **Blueprint topics covered in this chapter:** 

This chapter covers the following subtopics from the Cisco CCIE Routing and Switching written exam blueprint. Refer to the full blueprint in Table I-1 in the Introduction for more details on the topics covered in each chapter and their context within the blueprint. 

- IP Operation 

- TCP Operation 

- UDP Operation 

- IPv4 Addressing 

- IPv4 Subnetting 

- IPv4 VLSM 

- Route Summarization 

- NAT 

- IPv6 Addressing 

- IPv6 Subnetting 

- Migrating from IPv4 to IPv6

## **CHAPTER 4**

## **IP Addressing** 

Complete mastery of IP addressing and subnetting is required for any candidate to have a reasonable chance at passing both the CCIE written and lab exam. In fact, even the CCNA exam has fairly rigorous coverage of IP addressing and the related protocols. For the CCIE exam, understanding these topics is required to answer much deeper questions. For example, a question might ask for the interpretation of the output of a **show ip bgp** command and a configuration snippet to decide what routes would be summarized into a new prefix. To answer such questions, you must be familiar with the basic concepts and math behind subnetting .

## **“Do I Know This Already?” Quiz** 

Table  4-1 outlines the major headings in this chapter and the corresponding “Do I Know This Already?” quiz questions. 

**Table 4-1** _“Do I Know This Already?” Foundation Topics Section-to-Question Mapping_ 

|**Table 4-1** _“Do I Know This Alread_|_y?” Foundation Topics Section-to-Questio_|_n Mappin_|
|---|---|---|
|**Foundation Topics Section**|**Questions Covered in This Section**|**Score**|
|IP Addressing and Subnetting|1–4||
|CIDR, Private Addresses, and NAT|5–8||
|IPv6 Addressing and Tunneling|9–11||
|**Total Score**|||



To best use this pre-chapter assessment, remember to score yourself strictly. You can find the answers in  Appendix  A , “Answers to the ‘Do I Know This Already?’ Quizzes.” 

**1.** In what subnet does address 192.168.23.197/27 reside? 

   - **a.** 192.168.23.0 

   - **b.** 192.168.23.128 

   - **c.** 192.168.23.160 

   - **d.** 192.168.23.192 

   - **e.** 192.168.23.196 

184  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**2.** Router1 has four LAN interfaces, with IP addresses 10.1.1.1/24, 10.1.2.1/24, 10.1.3.1/24, and 10.1.4.1/24. What is the smallest summary route that could be advertised out a WAN link connecting Router1 to the rest of the network, if subnets not listed here were allowed to be included in the summary? 

   - **a.** 10.1.2.0/22 

   - **b.** 10.1.0.0/22 

   - **c.** 10.1.0.0/21 

   - **d.** 10.1.0.0/16 

**3.** Router1 has four LAN interfaces, with IP addresses 10.22.14.1/23, 10.22.18.1/23, 10.22.12.1/23, and 10.22.16.1/23. Which one of the answers lists the smallest summary route(s) that could be advertised by Router1 without also including subnets not listed in this question? 

   - **a.** 10.22.12.0/21 

   - **b.** 10.22.8.0/21 

   - **c.** 10.22.8.0/21 and 10.22.16.0/21 

   - **d.** 10.22.12.0/22 and 10.22.16.0/22 

**4.** Which two of the following VLSM subnets, when taken as a pair, overlap? 

   - **a.** 10.22.21.128/26 

   - **b.** 10.22.22.128/26 

   - **c.** 10.22.22.0/27 

   - **d.** 10.22.20.0/23 

   - **e.** 10.22.16.0/22 

**5.** Which of the following protocols or tools includes a feature like route summarization, plus administrative rules for global address assignment, with a goal of reducing the size of Internet routing tables? 

   - **a.** Classless interdomain routing 

   - **b.** Route summarization 

   - **c.** Supernetting 

   - **d.** Private IP addressing 

Chapter 4: IP Addressing  185 

**6.** Which of the following terms refer to a NAT feature that allows for significantly fewer IP addresses in the enterprise network as compared with the required public registered IP addresses? 

   - **a.** Static NAT 

   - **b.** Dynamic NAT 

   - **c.** Dynamic NAT with overloading 

   - **d.** PAT 

   - **e.** VAT 

**7.** Consider an enterprise network using private class A network 10.0.0.0, and using NAT to translate to IP addresses in registered class C network 205.1.1.0. Host 10.1.1.1 has an open www session to Internet web server 198.133.219.25. Which of the following terms refers to the destination address of a packet, sent by the web server back to the client, when the packet has not yet made it back to the enterprise’s NAT router? 

   - **a.** Inside Local 

   - **b.** Inside Global 

   - **c.** Outside Local 

   - **d.** Outside Global 

**8.** Router1 has its fa0/0 interface, address 10.1.2.3/24, connected to an enterprise network. Router1’s S0/1 interface connects to an ISP, with the interface using a publicly registered IP address of 171.1.1.1/30. Which of the following commands could be part of a valid NAT overload configuration, with 171.1.1.1 used as the public IP address? 

   - **a. ip nat inside source list 1 int s0/1 overload** 

   - **b. ip nat inside source list 1 pool fred overload** 

   - **c. ip nat inside source list 1 171.1.1.1 overload** 

   - **d.** None of the answers are correct. 

**9.** What feature is built into the IPv6 protocol to facilitate intranet-wide address management that enables a large number of IP hosts to easily discover the network and get new and globally unique IPv6 addresses associated with their location? 

   - **a.** ISATAP 

   - **b.** Address autoconfiguration 

   - **c.** Interface Overload 

   - **d.** None of the answers are correct. 

186  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**10.** What IPv6 transition strategy involves configuring devices to be able to run IPv4 and IPv6 simultaneously? 

   - **a.** ISATAP 

   - **b.** IPv4-in-IPv6 Tunnels 

   - **c.** Dual Stack 

   - **d.** 6to4 Tunnels 

**11.** If you use static configuration, all autoconfiguration features provided by IPv6 will be disabled. 

   - **a.** True 

   - **b.** False 

Chapter 4: IP Addressing  187 

**Foundation Topics**

## **IP Operation** 

IP is a protocol, and a protocol is best described as a series of rules governing how things work in a certain technologies, the ultimate goal being an operational standardization. When put into a network communication context, a protocol is the set of rules governing how packets are transmitted over a network. When you have a protocol, you are sure that all machines on a network (or in the world, when it comes to the Internet) speak the “same language” and can integrate into a holistic framework. IP is probably the most common protocol over the Internet. It is the set of rules governing how packets are transmitted over the Internet. 

The IP protocol standardizes the way that machines over the Internet or any IP network forward or route their packets based on their IP addresses. The most fundamental and basic operation we observe in IP is the ability to perform routing. The routing of IP packets and its unique addressing scheme is one of the main functions of the IP protocol. Routing consists of forwarding IP packets from source to destination machines over a network, based on their IP addresses. IP is probably the most common and widely used protocol in existence as a result of its ease and use, but IP on its own is not sufficient to every task that we might have in networking. It must be noted that the operation of IP is also governed by the manner in which we deliver what to packets. Yes, the routing protocol allows the delivery, but without certain additional components, IP will not, for example, provide reliable packet delivery. To meet this goal of adding features like reliable transport and acknowledgment, we need to rely on another feature known as Transport Control Protocol (TCP).

## **TCP Operation** 

When TCP couples with IP, you get a traffic controller that manages reliable exchange. TCP and IP work together to transmit data over the Internet, but at different levels. As we mentioned previously, IP does not guarantee reliable packet delivery over a network, and it is TCP that takes charge of making packet exchange reliable. 

TCP is the protocol that ensures reliability in a transmission with minimal loss of packets. Additional duties in the operation of TCP include assuring that packets maintain the right order, and that any delay is kept to an acceptable level. Also, it is TCP that prevents the possibility of packet duplication. All this is to ensure that the data received is consistent, in order, complete, and smooth. 

TCP operates in the protocol stack at the transport layer of the Open Systems Interconnection (OSI) model, which means that during data transmission, TCP works just before IP. TCP bundles data into TCP packets before sending these to IP, which in turn encapsulates these into IP packets. 

188  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

An IP packet is a packet of data that carries a data payload and an IP header. Any piece of data is broken into bits and placed into these packets and transmitted over the network. When the packets reach their destination, they are reassembled into the original data.

## **UDP Operation** 

The previous section discussed the nature of reliable transport that is provided by TCP, but there are instances in many networks where you either do not need reliable packet delivery or where you cannot afford to pay the associated costs of reliable delivery. Reliable packet delivery is slow, and many applications that can be deployed on a modern network find TCP too slow. A perfect example is voice and video traffic. But a more general explanation would be that TCP traffic is considered to be connection-oriented, whereas User Datagram Protocol (UDP) traffic is connectionless. This means that UDP packets do not contain anywhere near the amount of information as a TCP packet and thus they are smaller. This small size, coupled with their speed, makes them ideal for applications that are sensitive to the packet loss or delay such as IP voice or video solutions. 

But no matter the transport method, TCP or UDP, your IP packets are delivered and managed in the context of IOS through their unique logical addressing and the ability to partition sections of addresses into usable networks.

## **IP Addressing and Subnetting** 

You need a postal address to receive letters; similarly, computers must use an IP address to be able to send and receive data using the TCP/IP protocols. Just as the postal service dictates the format and meaning of a postal address to aid the efficient delivery of mail, the TCP/IP protocol suite imposes some rules about IP address assignment so that routers can efficiently forward packets between IP hosts. This chapter begins with coverage of the format and meaning of IP addresses, with required consideration for how they are grouped to aid the routing process.

## **IP Addressing and Subnetting Review** 

First, here’s a quick review of some of the core facts about IPv4 addresses that should be fairly familiar to you: 

- A 32-bit binary number. 

- Written in “dotted decimal” notation (for example, 1.2.3.4), with each decimal octet representing 8 bits. 

- Addresses are assigned to network interfaces, so computers or routers with multiple interfaces have multiple IP addresses. 

- A computer with an IP address assigned to an interface is an _IP host_ . 

Chapter 4: IP Addressing  189 

**Key Topic** 

- A group of IP hosts that are not separated from each other by an IP router are in the same grouping. 

- These groupings are called _networks_ , _subnets_ , or _prefixes_ , depending on the context. 

- IP hosts separated from another set of IP hosts by a router must be in separate groupings (network/subnet/prefix). 

IP addresses can be analyzed using _classful_ or _classless_ logic, depending on the situation. Classful logic simply means that the main class A, B, and C rules from RFC 791 are considered. The next several pages present a classful view of IP addresses, as reviewed in Table  4-2 . 

With classful addressing, class A, B, and C networks can be identified as such by their first several bits (shown in the last column of  Table  4-2 ) or by the range of decimal values for their first octets. Also, each class A, B, or C address has two parts (when not subnetted): a _network part_ and a _host part_ . The size of each is implied by the class, and can be stated explicitly using the default mask for that class of network. For example, mask 255.0.0.0, the default mask for class A networks, has 8 binary 1s and 24 binary 0s, representing the size of the network and host parts, respectively. 

**Table 4-2** _Classful Network Review_ 

|**Table 4-2**|_Classful Network Rev_|_iew_|||
|---|---|---|---|---|
|**Class of**|**Size of Network and**|**Range of First**|**Default Mask for**|**Identifying Bits**|
|**Address**|**Host Parts of the**|**Octet Values**|**Each Class of**|**at Beginning of**|
||**Addresses**||**Network**|**Address**|
|A|8/24|1–126|255.0.0.0|0|
|B|16/16|128–191|255.255.0.0|10|
|C|24/8|192–223|255.255.255.0|110|
|D|—|224–239|—|1110|
|E|—|240–255|—|1111|

## Subnetting a Classful Network Number 

With classful addressing, and no subnetting, an entire class A, B, or C network is needed on each individual instance of a data link. For example,  Figure  4-1 shows a sample internetwork, with dashed-line circles representing the set of hosts that must be in the same IP network—in this case requiring three networks.  Figure  4-1 shows two options for how IP addresses can be assigned and grouped together for this internetwork topology. 

190  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Option 1: Use Classful Networks for Each Group 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0231-02.png)


**----- Start of picture text -----**<br>
Network 172.31.0.0 Network 130.2.0.0 Network 8.0.0.0<br>Client3<br>E0/0 R3 R1 SW1<br>172.31.103.41<br>Subnet 172.31.103.0 Subnet 172.31.13.0 Subnet 172.31.11.0<br>255.255.255.0 255.255.255.0 255.255.255.0<br>**----- End of picture text -----**<br>


Option 2: Use Subnets of One Classful Network 

**Figure 4-1** _Sample Internetwork with Two Alternatives for Address Assignment— Without and With Subnetting_ 

Option 1 uses three classful networks; however, it wastes a lot of IP addresses. For example, all hosts in class A network 8.0.0.0 must reside on the LAN on the right side of the figure. 

Of course, the much more reasonable alternative is to reserve one classful IP network number and use _subnetting_ to subdivide that network into at least three subdivisions, called _subnets_ . Option 2 (bottom of  Figure  4-1 ) shows how to subdivide a class A, B, or C network into subnets. 

To create subnets, the IP addresses must have three fields instead of just two—the network, _subnet_ , and host. When using classful logic to interpret IP addresses, the size of the network part is still defined by classful rules—either 8, 16, or 24 bits based on class. To create the subnet field, the host field is shortened, as shown in  Figure  4-2 . 

|8|24 – x|24 – x|x|x|x|
|---|---|---|---|---|---|
|Network|Subnet||Host|||
|16<br>16 – x<br>x||||||
|Network||Subnet||Host||
|x<br>8 – x<br>24||||||
|Network|||Subnet||Host|



**Figure 4-2** _Formats of IP Addresses when Subnetting_ 

Chapter 4: IP Addressing  191 

**Key Topic** 

**Note** The term _internetwork_ refers to a collection of computers and networking hardware; because TCP/IP discussions frequently use the term _network_ to refer to a classful class A, B, or C IP network, this book uses the term _internetwork_ to refer to an entire network topology, as shown in Figure 4-1. 

To determine the size of each field in a subnetted IP address, you can follow the three easy steps shown in  Table  4-3 . Note that  Figure  4-1 also showed alternative addressing for using subnets, with the last column in  Table  4-3 showing the size of each field for that particular example, which used class B network 172.31.0.0, mask 255.255.255.0. 

**Table 4-3** _Finding the Size of the Network, Subnet, and Host Fields in an IP Address_ 

|**Name of Part of**|**Process to Find Its Size**|**Size per  Figure  4-1**|
|---|---|---|
|**the Address**||**Example**|
|Network|8, 16, or 24 bits based on class rules|16|
|Subnet|32 minus network and host bits|8|
|Host|Equal to the number of binary 0s in the mask|8|

## Comments on Classless Addressing 

The terms _classless_ and _classful_ can be applied to three popular topics that are all related to IP. This chapter explains classful and classless IP addressing, which are relatively simple concepts. Two other chapters explain the other uses of the terms classless and classful: Chapter  6 , “IP Forwarding (Routing),” describes classless/classful routing, and  Chapter  7 , “RIPv2 and RIPng,” covers classless/classful routing protocols. 

Classless IP addressing, simply put, means that class A, B, and C rules are ignored. Each address is viewed as a two-part address, formally called the _prefix_ and the _host_ parts of the address. The prefix simply states how many of the beginning bits of an IP address identify or define the group. It is the same idea as using the combined network and subnet parts of an address to identify a subnet. All the hosts with identical prefixes are in effect in the same group, which can be called a _subnet_ or a _prefix_ . 

Just as a classful subnet must be listed with the subnet mask to know exactly which addresses are in the subnet, a prefix must be listed with its _prefix length_ . The prefix itself is a dotted-decimal number. It is typically followed by a / symbol, after which the prefix length is listed. The prefix length is a decimal number that denotes the length (in bits) of the prefix. For example, 172.31.13.0/24 means a prefix of 172.31.13.0 and a prefix length of 24 bits. Also, the prefix can be implied by a subnet mask, with the number of 1s in the binary version of the mask implying the prefix length. 

Classless and classful addressing are mainly just two ways to think about IP address formats. For the exam, make sure to understand both perspectives and the terminology used by each. 

192  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Subnetting Math** 

Knowing how to interpret the meaning of addresses and masks, routes and masks in the routing table, and addresses and masks in access control lists (ACL) and how to configure route filtering are all very important topics for the CCIE Routing and Switching written and lab exams. This section covers the binary math briefly, with coverage of some tricks to do the math quickly without binary math. Several subsequent chapters cover the configuration details of features that require this math.

## Dissecting the Component Parts of an IP Address 

First, deducing the size of the three parts (classful view) or two parts (classless view) of an IP address is important, because it allows you to analyze information about that subnet and other subnets. Every internetwork requires some number of subnets, and some number of hosts per subnet. Analyzing the format of an existing address, based on the mask or prefix length, enables you to determine whether enough hosts per subnet exist, or whether enough subnets exist to support the number of hosts. The following list summarizes some of the common math facts about subnetting related to the format of IP addresses: 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0233-05.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


- If a subnet has been defined with _y_ host bits, there are 2 _y_ – 2 valid usable IP addresses in the subnet, because two numeric values are reserved. 

- One reserved IP address in each subnet is the subnet number itself. This number, by definition, has binary 0s for all host bits. This number represents the subnet, and is typically seen in routing tables. 

- The other reserved IP address in the subnet is the subnet broadcast address, which by definition has binary 1s for all host bits. This number can be used as a destination IP address to send a packet to all hosts in the subnet. 

- When you are thinking classfully, if the mask implies _x_ subnet bits, then 2 _x_ possible subnets exist for that classful network, assuming that the same mask is used throughout the network. 

- Although there are no truly reserved values for the subnet numbers, two (lowest and highest values) can be discouraged from use in some cases: 

   - **Zero subnet:** The subnet fi eld is all binary 0s; in decimal, each zero subnet is the exact same dotted-decimal number as the classful network number, potentially causing confusion. 

   - **Broadcast subnet:** The subnet fi eld is all binary 1s; in decimal, this subnet’s broadcast address is the same as the network-wide broadcast address, potentially causing confusion. 

In Cisco routers, by default, zero subnets and broadcast subnets work fine. You can disable the use of the zero subnet with the **no ip subnet-zero** global command. The only time that using the zero subnet typically causes problems is when classful routing protocols are used. 

Chapter 4: IP Addressing  193 

**Key Topic**

## Finding Subnet Numbers and Valid Range of IP Addresses—Binary 

When examining an IP address and mask, the process of finding the subnet number, the broadcast address, and the range of valid IP addresses is as fundamental to networking as is addition and subtraction for advanced math. Possibly more so for the CCIE Routing and Switching lab exam, mastery of the math behind subnetting, which is the same basic math behind route summarization and filtering, will improve your speed in completing complex configurations on the exam. 

The range of valid IP addresses in a subnet begins with the number that is 1 larger than the subnet number, and ends with the address that is 1 smaller than the broadcast address for the subnet. So, to determine the range of valid addresses, just calculate the subnet number and broadcast address, which can be done as follows: 

- **To derive the subnet number:** Perform a bitwise Boolean AND between the IP address and mask. 

- **To derive the broadcast address:** Change all host bits in the subnet number from 0s to 1s. 

A bitwise Boolean AND means that you place two long binary numbers on top of each other, and then AND the two bits that line up vertically. (A Boolean AND results in a binary 1 only if both bits are 1; otherwise, the result is 0.)  Table  4-4 shows an easy example based on subnet 172.31.103.0/24 from  Figure  4-1 . 

**Table 4-4** _Binary Math to Calculate the Subnet Number and Broadcast Address_ 

|**Table 4-4** _Binary Math_|_to Calculate the S_|_ubnet Number and Broadcast Address_|
|---|---|---|
|**Address**|172.31.103.41|1010 1100 0001 1111 0110 0111**0010 1001**|
|**Mask**|255.255.255.0|1111 1111 1111 1111 1111 1111**0000 0000**|
|**Subnet Number (Result**|172.31.103.0|1010 1100 0001 1111 0110 0111**0000 0000**|
|**of AND)**|||
|**Broadcast**|172.31.103.255|1010 1100 0001 1111 0110 0111**1111 1111**|



Probably almost everyone reading this already knew that the decimal subnet number and broadcast addresses shown in  Table  4-4 were correct, even without looking at the binary math. The important part is to recall the binary process, and practice until you can confidently and consistently find the answer without using any binary math. The only parts of the math that typically trip people up are the binary-to-decimal and decimal-to-binary conversions. When working in binary, keep in mind that you will not have a calculator for the written exam, and that when converting to decimal, you always convert 8 bits at a time—even if an octet contains some prefix bits and some host bits. ( Appendix  C , “Decimal-to-Binary Conversion Table,” contains a conversion table for your reference.) 

194  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## Decimal Shortcuts to Find the Subnet Number and Valid Range of IP Addresses 

Many of the IP addressing and routing related problems on the exam come back to the ability to solve a couple of classic basic problems. One of those problems runs as follows: 

Given an IP address and mask (or prefix length), determine the subnet number/prefix, broadcast address, and range of valid IP addresses. 

If you can already solve such problems with only a few seconds’ thought, even with tricky masks, you can skip this section of the chapter. If you cannot solve such questions easily and quickly, this section can help you learn some math shortcuts that allow you to find the answers without needing to use any Boolean math. 

**Note** The next several pages of this chapter describe some algorithms that you can use to find many important details related to IP addressing, without needing to convert to and from binary. In my experience, some people simply work better performing the math in binary until the answers simply start popping into their heads. Others find that the decimal shortcuts are more effective. 

If you use the decimal shortcuts, it is best to practice them until you no longer really use the exact steps listed in this book; rather, the processes should become second nature. To that end, CD-only Appendix D, “IP Addressing Practice,” lists several practice problems for each of the algorithms presented in this chapter. 

To solve the “find the subnet/broadcast/range of addresses” type of problem, at least three of the four octets should have pretty simple math. For example, with a nice, easy mask like 255.255.255.0, the logic used to find the subnet number and broadcast address is intuitive to most people. The more challenging cases occur when the mask or prefix does not divide the host field at a byte boundary. For example, the same IP address 172.31.103.41, with mask 255.255.252.0 (prefix /22), is actually in subnet 172.31.100.0. Working with the third octet in this example is the hard part, because the mask value for that octet is not 0 or 255; for the upcoming process, this octet is called the _interesting octet_ . The following process finds the subnet number, using decimal math, even with a challenging mask: 

- **Step 1.** Find the mask octets of value 255; copy the same octets from the IP address. 

- **Step 2.** Find the mask octets of value 0; write down 0s for the same octets. 

- **Step 3.** If one octet has not yet been filled in, that octet is the interesting octet. Find the subnet mask’s value in the interesting octet and subtract it from 256. Call this number the “magic number.” 

- **Step 4.** Find the integer multiple of the magic number that is closest to, but not larger than, the interesting octet’s value. 

Chapter 4: IP Addressing  195 

An example certainly helps, as shown in  Table  4-5 , with 172.31.103.41, mask 255.255.252.0. The table separates the address into its four component octets. In this example, the first, second, and fourth octets of the subnet number are easily found from Steps 1 and 2 in the process. Because the interesting octet is the third octet, the magic number is 256 – 252, or 4. The integer multiple of 4, closest to 103 but not exceeding 103, is 100—making 100 the subnet number’s value in the third octet. (Note that you can use this same process even with an easy mask, and Steps 1 and 2 will give you the complete subnet number.) 

**Table 4-5** _Quick Math to Find the Subnet Number—172.31.103.41, 255.255.252.0_ 

|**Table 4-5** _Quick Math to Fin_|_d the S_|_ubnet Numbe_|_ubnet Numbe_|_r—17_|_2.31.103.41, 255.255.252.0_|
|---|---|---|---|---|---|
|||**Octet**|||**Comments**|
||**1**|**2**|**3**|**4**||
|**Address**|172|31|103|41||
|**Mask**|255|255|252|0|Equivalent to /22.|
|**Subnet number results after**|172|31||0|Magic number will be 256 –|
|**Steps 1 and 2**|||||252 = 4.|
|**Subnet number after complet-**|172|31|**100**|0|100 is the multiple of 4 closest|
|**ing the interesting octet**|||||to, but not exceeding, 103.|



A similar process can be used to determine the subnet broadcast address. This process assumes that the mask is tricky. The detailed steps are as follows: 

- **Step 1.** Start with the subnet number. 

- **Step 2.** Decide which octet is interesting, based on which octet of the mask does not have a 0 or 255. 

- **Step 3.** For octets to the left of the interesting octet, copy the subnet number’s values into the place where you are writing down the broadcast address. 

- **Step 4.** For any octets to the right of the interesting octet, write 255 for the broadcast address. 

- **Step 5.** Calculate the magic number: Find the subnet mask’s value in the interesting octet and subtract it from 256. 

- **Step 6.** Take the subnet number’s interesting octet value, add the magic number to it, and subtract 1. Fill in the broadcast address’s interesting octet with this number. 

Table  4-6 shows the 172.31.103.41/22 example again, using this process to find the subnet broadcast address. 

196  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 4-6** _Quick Math to Find the Broadcast Address—172.31.103.41, 255.255.252.0_ 

|||**Octet**|**Octet**||**Comments**|
|---|---|---|---|---|---|
||**1**|**2**|**3**|**4**||
|**Subnet number (per Step 1) **|172|31|100|0||
|**Mask (for reference)**|255|255|252|0|Equivalent to /22|
|**Results after Steps 1 to 4**|172|31||255|Magic number will be 256 – 252 = 4|
|**Subnet number after**|172|31|**103 **|255|Subnet’s third octet (100), plus magic|
|**completing the empty octet**|||||number (4), minus 1 is 103|



**Note** If you have read the last few pages to improve your speed at dissecting a subnet without requiring binary math, it is probably a good time to pull out the CD in the back of the book. CD-only Appendix D, “IP Addressing Practice,” contains several practice problems for finding the subnet and broadcast address, as well as for many other math issues related to IP addressing.

## Determining All Subnets of a Network—Binary 

Another common question, typically simply a portion of a more challenging question on the CCIE written exam, relates to finding all subnets of a network. The base underlying question might be as follows: 

Given a particular class A, B, or C network, and a mask/prefix length used on all subnets of that network, what are the actual subnet numbers? 

The answers can be found using binary or using a simple decimal algorithm. This section first shows how to answer the question using binary, using the following steps. Note that the steps include details that are not really necessary for the math part of the problem; these steps are mainly helpful for practicing the process. 

**Key Topic** 

- **Step 1.** Write the binary version of the classful network number; that value is actually the zero subnet as well. 

- **Step 2.** Draw two vertical lines through the number, one separating the network and subnet parts of the number, the other separating the subnet and host part. 

- **Step 3.** Calculate the number of subnets, including the zero and broadcast subnet, based on 2 _y_ , where _y_ is the number of subnet bits. 

- **Step 4.** Write _y_ −1 copies of the binary network number below the first one, but leave the subnet field blank. 

- **Step 5.** Using the subnet field as a binary counter, write the values, top to bottom, in which the next value is 1 greater than the previous. 

- **Step 6.** Convert the binary numbers, 8 bits at a time, back to decimal. 

Chapter 4: IP Addressing  197 

This process takes advantage of a couple of facts about the binary form of IP subnet numbers: 

- All subnets of a classful network have the same value in the network portion of the subnet number. 

- All subnets of any classful network have binary 0s in the host portion of the subnet number. 

Step 4 in the process simply makes you write the network and host parts of each subnet number, because those values are easily predicted. To find the different subnet numbers, you then just need to discover all possible different combinations of binary digits in the subnet field, because that is the only part of the subnet numbers that differs from subnet to subnet. 

For example, consider the same class B network 172.31.0.0, with static length subnet masking (SLSM) assumed, and a mask of 255.255.224.0. Note that this example uses 3 subnet bits, so there will be 23 subnets.  Table  4-7 lists the example. 

**Table 4-7** _Binary Method to Find All Subnets—Steps 1 Through 4_ 

|**Table 4-7** _Binary Method to Find_|_All Subnets—S_|_teps_|_1 Through 4_|_1 Through 4_||
|---|---|---|---|---|---|
||||**Octet**|||
|**Subnet**|**1**|**2**||**3**|**4**|
|**Network number/zero subnet**|10101100|000|11111|000|00000  00000000|
|**2nd subnet**|10101100|000|11111||00000  00000000|
|**3rd subnet**|10101100|000|11111||00000  00000000|
|**4th subnet**|10101100|000|11111||00000  00000000|
|**5th subnet**|10101100|000|11111||00000  00000000|
|**6th subnet**|10101100|000|11111||00000  00000000|
|**7th subnet**|10101100|000|11111||00000  00000000|
|**8th subnet (2****_y_ = 8); broadcast subnet **10101100||000|11111||00000  00000000|



At this point, you have the zero subnet recorded at the top, and you are ready to use the subnet field (the missing bits in the table) as a counter to find all possible values.  Table 4-8 completes the process. 

198  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 4-8** _Binary Method to Find All Subnets—Step 5_ 

|||**Octet**|**Octet**||
|---|---|---|---|---|
|**Subnet**|**1**|**2**|**3**|**4**|
|**Network number/zero subnet**|10101100|00011111|**000 **00000|00000000|
|**2nd subnet**|10101100|00011111|**001 **00000|00000000|
|**3rd subnet**|10101100|00011111|**010 **00000|00000000|
|**4th subnet**|10101100|00011111|**011 **00000|00000000|
|**5th subnet**|10101100|00011111|**100 **00000|00000000|
|**6th subnet**|10101100|00011111|**101 **00000|00000000|
|**7th subnet**|10101100|00011111|**110 **00000|00000000|
|**8th subnet (2****_y_ = 8); broadcast subnet **10101100||00011111|**111 **00000|00000000|



The final step to determine all subnets is simply to convert the values back to decimal. Take care to always convert 8 bits at a time. In this case, you end up with the following subnets: 172.31.0.0, 172.31.32.0, 172.31.64.0, 172.31.96.0, 172.31.128.0, 172.31.160.0, 172.31.192.0, and 172.31.224.0.

## Determining All Subnets of a Network—Decimal 

You might have noticed the trend in the third octet values in the subnets listed in the previous paragraph. When assuming SLSM, the subnet numbers in decimal do have a regular increment value, which turns out to be the value of the magic number. For example, instead of the binary math in the previous section, you could have thought the following: 

- The interesting octet is the third octet. 

- The magic number is 256 – 224 = 32. 

- 172.31.0.0 is the zero subnet, because it is the same number as the network number. 

- The other subnet numbers are increments of the magic number inside the interesting octet. 

If that logic already clicks in your head, you can skip to the next section in this chapter. If not, the rest of this section outlines a decimal algorithm that takes a little longer pass at the same general logic. First, the question and the algorithm assume that the same subnet mask is used on all subnets of this one classful network—a feature sometimes called _static length subnet masking (SLSM)_ . In contrast, _variable length subnet masking (VLSM)_ means that different masks are used in the same classful network. The algorithm assumes a subnet field of 8 bits or less just to keep the steps uncluttered; for longer subnet fields, the algorithm can be easily extrapolated. 

Chapter 4: IP Addressing  199 

- **Step 1.** Write the classful network number in decimal. 

**Key Topic** 

- **Step 2.** For the first (lowest numeric) subnet number, copy the entire network number. That is the first subnet number, and is also the zero subnet. 

- **Step 3.** Decide which octet contains the entire subnet field; call this octet the interesting octet. (Remember, this algorithm assumes 8 subnet bits or less, so the entire subnet field will be in a single interesting octet.) 

- **Step 4.** Calculate the magic number by subtracting the mask’s interesting octet value from 256. 

- **Step 5.** Copy the previous subnet number’s noninteresting octets onto the next line as the next subnet number; only one octet is missing at this point. 

- **Step 6.** Add the magic number to the previous subnet’s interesting octet, and write that as the next subnet number’s interesting octet, completing the next subnet number. 

- **Step 7.** Repeat Steps 5 and 6 until the new interesting octet is 256. That subnet is not valid. The previously calculated subnet is the last valid subnet, and also the broadcast subnet. 

For example, consider the same class B network 172.31.0.0, with SLSM assumed, and a mask of 255.255.224.0.  Table  4-9 lists the example. 

**Table 4-9** _Subnet List Chart—172.31.0.0/255.255.224.0_ 

|||**Octet**|**Octet**||**Comments**|
|---|---|---|---|---|---|
||**1**|**2**|**3**|**4**||
|**Network number**|172|31|0|0|Step 1 from the process.|
|**Mask**|255|255|224|0|Magic number is 256 – 224 = 32.|
|**Subnet zero**|172|31|0|0|Step 2 from the process.|
|**First subnet**|172|31|32|0|Steps 5 and 6; previous interesting octet 0,|
||||||plus magic number (32).|
|**Next subnet**|172|31|64|0|32 plus magic number is 64.|
|**Next subnet**|172|31|96|0|64 plus magic number is 96.|
|**Next subnet**|172|31|128|0|96 plus magic number is 128.|
|**Next subnet**|172|31|160|0|128 plus magic number is 160.|
|**Next subnet**|172|31|192|0|160 plus magic number is 192.|
|**Last subnet (broadcast)**|172|31|224|0|The broadcast subnet in this case.|
|**Invalid; easy-to-**|172|31|256|0|256 is out of range; when writing this one,|
|**recognize stopping point**|||||note that it is invalid, and that the previous|
||||||one is the last valid subnet.|



200  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

You can use this process repeatedly as needed until the answers start jumping out at you without the table and step-wise algorithm. For more practice, refer to CD-only  Appendix  D .

## **VLSM Subnet Allocation** 

So far in this chapter, most of the discussion has been about examining existing ad - dresses and subnets. Before deploying new networks, or new parts of a network, you must give some thought to the ranges of IP addresses to be allocated. Also, when assigning subnets for different locations, you should assign the subnets with thought for how routes could then be summarized. This section covers some of the key concepts related to subnet allocation and summarization. (This section focuses on the concepts behind summarization; the configuration of route summarization is routing protocol–specific and thus is covered in the individual chapters covering routing protocols.) 

Many organizations purposefully use SLSM to simplify operations. Additionally, many internetworks also use private IP network 10.0.0.0, with an SLSM prefix length of /24, and use NAT for connecting to the Internet. Operations and troubleshooting can be a lot easier when you use SLSM, particularly with a nice, easy prefix like /24. 

In some cases, VLSM is required or preferred when allocating addresses. VLSM is typically chosen when the address space is constrained to some degree. The VLSM subnet assignment strategy covered here complies with the strategy you might remember from the Cisco BSCI course or from reading the Cisco Press CCNP Routing certification books. 

Similar to when assigning subnets with SLSM, you should use an easily summarized block of addresses for a new part of the network. Because VLSM network addresses are likely constrained to some degree, you should choose the specific subnets wisely. The general rules for choosing wisely are as follows:

## **Key Topic** 

- **Step 1.** Determine the shortest prefix length (in other words, the largest block) required. 

- **Step 2.** Divide the available address block into equal-sized prefixes based on the shortest prefix from Step 1. 

- **Step 3.** Allocate the largest required subnets/prefixes from the beginning of the IP address block, leaving some equal-sized unallocated address blocks at the end of the original large address block. 

- **Step 4.** Choose an unallocated block that you will further subdivide by repeating the first three steps, using the shortest required prefix length (largest address block) for the remaining subnets. 

- **Step 5.** When allocating very small address blocks for use on links between routers, consider using subnets at the end of the address range. This leaves the largest consecutive blocks available in case future requirements change. 

For example, imagine that a network engineer plans a new site installation. He allocates the 172.31.28.0/23 address block for the new site, expecting to use the block as a single summarized route. When planning, the engineer then subdivides 172.31.28.0/23 per the 

Chapter 4: IP Addressing  201 

**Key Topic** 

subnet requirements for the new installation, as shown in  Figure  4-3 . The figure shows three iterations through the VLSM subnet assignment process, because the requirements call for three different subnet sizes. Each iteration divides a remaining block into equal sizes, based on the prefix requirements of the subnets allocated at that step. Note that the small /30 prefixes were allocated from the end of the address range, leaving the largest possible consecutive address range for future growth.

## **172.31.28.0/23 (172.31.28.0 Through 172.31.29.255) Requirements:** 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0242-04.png)


**----- Start of picture text -----**<br>
3 /25’s<br>2 /27’s<br>3 /30’s<br>**----- End of picture text -----**<br>


**Pass 1: /25 prefixes Block 172.31.28.0/23** 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0242-06.png)


**----- Start of picture text -----**<br>
Allocated Allocated Allocated Unallocated<br>172.31.28.0/25 172.31.28.128/25 172.31.29.0/25 172.31.29.128/25<br>172.31.28.1 – 172.31.28.129 – 172.31.29.1 – 172.31.29.129 –<br>172.31.28.126 172.31.28.254 172.31.29.126 172.31.29.254<br>Pass 2: /27 prefixes Allocated Allocated Unallocated Unallocated<br>Block 172.31.29.128/25<br>172.31.29.128/27 172.31.29.160/27 172.31.29.192/27 172.31.29.224/27<br>Unallocated Allocated<br>Step 3: /30 prefixes<br>Allocate High End:<br>172.31.29.252/30,<br>172.31.29.248/30,<br>172.31.29.244/30<br>**----- End of picture text -----**<br>


**Figure 4-3** _Example of VLSM Subnet Allocation Process_

## **Route Summarization Concepts** 

The ability to recognize and define how to most efficiently summarize existing address ranges is an important skill on both the written and lab exams. For the written exam, the question might not be as straightforward as, “What is the most efficient summarization of the following subnets?” Rather, the math required for such a question might simply be part of a larger question. Certainly, such math is required for the lab exam. This section looks at the math behind finding the best summarization; other chapters cover specific configuration commands. 

Good IP address assignment practices should always consider the capabilities for route summarization. For example, if a division of a company needs 15 subnets, an engineer needs to allocate those 15 subnets from the unused portions of the address block available to that internetwork. However, assigning subnets 10.1.101.0/24 through 10.1.115.0/24 would be a poor choice, because those do not easily summarize. Rather, allocate a range of addresses that can be easily summarized into a single route. For example, subnets 

202  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

10.1.96.0/24 through 10.1.111.0/24 can be summarized as a single 10.1.96.0/20 route, making those routes a better choice. 

There are two main ways to think of the word _best_ when you are looking for the “best summarization”: 

- **Inclusive summary routes:** A single summarized route that is as small a range of addresses as possible, while including all routes/subnets shown, and _possibly including subnets that do not currently exist._ 

- **Exclusive summary routes:** As few as possible summarized routes that include all to-be-summarized address ranges, but _excluding all other routes/subnets._ 

**Note** The terms _inclusive summary_ , _exclusive summary_ , and _candidate summary_ are simply terms I invented for this book and will continue to use later in the chapter. 

For example, with the VLSM example in  Figure  4-3 , the network engineer purposefully planned so that an inclusive summary of 172.31.28.0/23 could be used. Even though not all subnets are yet allocated from that address range, the engineer is likely saving the rest of that address range for future subnets at that site, so summarizing using an inclusive summary is reasonable. In other cases, typically when trying to summarize routes in an internetwork for which summarization was not planned, the summarization must exclude routes that are not explicitly listed, because those address ranges can actually be used in another part of the internetwork.

## Finding Inclusive Summary Routes—Binary 

Finding the best inclusive summary lends itself to a formal binary process, as well as to a formal decimal process. The binary process runs as follows: 

- **Step 1.** Write the binary version of each component subnet, one on top of the other. 

- **Step 2.** Inspect the binary values to find how many consecutive bits have the exact same value in all component subnets. That number of bits is the prefix length. 

- **Step 3.** Write a new 32-bit number at the bottom of the list by copying _y_ bits from the prior number, _y_ being the prefix length. Write binary 0s for the remaining bits. This is the inclusive summary. 

- **Step 4.** Convert the new number to decimal, 8 bits at a time. 

Table  4-10 shows an example of this process, using four routes, 172.31.20.0, .21.0, .22.0, and .23.0, all with prefix /24. 

Chapter 4: IP Addressing  203 

**Table 4-10** _Example of Finding the Best Inclusive Summary—Binary_ 

||**Octet 1**|**Octet 2**|**Octet 3**|**Octet 4**|
|---|---|---|---|---|
|**172.31.20.0/24**|10101100|00011111|000101 00|00000000|
|**172.31.21.0/24**|10101100|00011111|000101 01|00000000|
|**172.31.22.0/24**|10101100|00011111|000101 10|00000000|
|**172.31.23.0/24**|10101100|00011111|000101 11|00000000|
|**Prefix length: 22**|||||
|**Inclusive summary**|10101100|00011111|000101**00**|**00000000**|



The trickiest part is Step 2, in which you have to simply look at the binary values and find the point at which the bits are no longer equal. You can shorten the process by, in this case, noticing that all component subnets begin with 172.31, meaning that the first 16 bits will certainly have the same values.

## Finding Inclusive Summary Routes—Decimal 

To find the same inclusive summary using only decimal math, use the following process. The process works just fine with variable prefix lengths and nonconsecutive subnets. 

- **Step 1.** Count the number of subnets; then, find the smallest value of _y_ , such that 2 _y_ => that number of subnets. 

- **Step 2.** For the next step, use a prefix length based on the longest prefix length of the component subnets, minus _y_ . 

- **Step 3.** Pretend that the lowest numeric subnet number in the list of component subnets is an IP address. Using the new, smaller prefix from Step 2, calculate the subnet number in which this pretend address resides. 

- **Step 4.** Repeat Step 3 for the largest numeric component subnet number and the same prefix. If it is the same subnet derived as in Step 3, the resulting subnet is the best summarized route, using the new prefix. 

- **Step 5.** If Steps 3 and 4 do not yield the same resulting subnet, repeat Steps 3 and 4 with another new prefix length of 1 less than the last prefix length. 

Table  4-11 shows two examples of the process. The first example has four routes, 172.31.20.0, .21.0, .22.0, and .23.0, all with prefix /24. The second example adds 172.31.24.0 to that same list. 

204  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 4-11** _Example of Finding the Best Summarizations_ 

|**Step**|**Range of .20.0, .21.0, .22.0,**|**Same Range, Plus 172.31.24.0**|
|---|---|---|
||**and .23.0, /24**||
|Step 1|22 = 4,_y_= 2|23 = 8,_y_= 3|
|Step 2|24 – 2 = 22|24 – 3 = 21|
|Step 3|Smallest subnet 172.31.20.0, with|Smallest subnet 172.31.20.0, with /21,|
||/22, yields**172.31.20.0/22**|yields**172.31.16.0/21**|
|Step 4|Largest subnet 172.31.23.0, with|Largest subnet 172.31.24.0, with /21,|
||/22, yields**172.31.20.0/22**|yields**172.31.24.0/21**|
|Step 5|—|21 – 1 = 20; new prefix|
|Step 3, 2nd time  —||172.31.16.0/20|
|Step 4, 2nd|—|172.31.16.0/20; the same as prior step,|
|time||so that is the answer|



With the first example, Steps 3 and 4 yielded the same answer, which means that the best inclusive summary had been found. With the second example, a second pass through the process was required. CD-only  Appendix  D contains several practice problems to help you develop speed and make this process second nature.

## Finding Exclusive Summary Routes—Binary 

A similar process, listed next, can be used to find the exclusive summary. Keep in mind that the best exclusive summary can be composed of multiple summary routes. Once again, to keep it simple, the process assumes SLSM. 

- **Step 1.** Find the best _exclusive_ summary route; call it a _candidate exclusive_ summary route. 

- **Step 2.** Determine whether the candidate summary includes any address ranges it should not. To do so, compare the summary’s implied address range with the implied address ranges of the component subnets. 

- **Step 3.** If the candidate summary only includes addresses in the ranges implied by the component subnets, the candidate summary is part of the best exclusive summarization of the original component subnets. 

- **Step 4.** If instead the candidate summary includes some addresses that match the candidate summary routes and some addresses that do not, split the current candidate summary in half, into two new candidate summary routes, each with a prefix 1 _longer_ than before. 

- **Step 5.** If the candidate summary only includes addresses outside the ranges implied by the component subnets, the candidate summary is not part of the best exclusive summarization, and it should not be split further. 

Chapter 4: IP Addressing  205 

**Step 6.** Repeat Steps 2 through 4 for each of the two possible candidate summary routes created at Step 4. 

For example, take the same five subnets used with the inclusive example—172.31.20.0/24, .21.0, .22.0, .23.0, and .24.0. The best inclusive summary is 172.31.16.0/20, which implies an address range of 172.31.16.0 to 172.31.31.255—clearly, it includes more addresses than the original five subnets. So, repeat the process of splitting the summary in half, and repeating, until summaries are found that do not include any unnecessary address ranges. Figure  4-4 shows the idea behind the logic. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0246-03.png)


**----- Start of picture text -----**<br>
Routes to Summarize:<br>172.31.20.0/24 (20.0 thru 20.255)<br>172.31.21.0/24 (21.0 thru 21.255)<br>172.31.22.0/24 (22.0 thru 22.255) 172.31.16.0/20: 16.0 Thru 31.255<br>172.31.23.0/24 (23.0 thru 23.255) Too Inclusive:<br>172.31.24.0/24 (24.0 thru 24.255)<br>Split!<br>172.31.16.0/21: 16.0 thru 23.255 172.31.24.0/21: 24.0 thru 31.255<br>Too Inclusive: Too Inclusive:<br>Split! Split!<br>172.31.16.0/22: 172.31.20.0/22: 172.31.24.0/22: 172.31.28.0/22:<br>16.0 Thru 19.255 20.0 Thru 23.255 24.0 Thru 27.255 28.0 Thru 31.255<br>Range completely Range is Too inclusive: Range completely<br>outside range to exclusively from keep splitting! outside range to<br>be summarized; target range – (Details not be summarized;<br>stop splitting. keep this as part shown.) stop splitting.<br>of best exclusive<br>summary!<br>**----- End of picture text -----**<br>


**Figure 4-4** _Example of Process to Find Exclusive Summary Routes_ 

The process starts with one candidate summary. If it includes some addresses that need to be summarized and some addresses it should not summarize, split it in half and try again with each half. Eventually, the best exclusive summary routes are found, or the splitting keeps happening until you get back to the original routes. In fact, in this case, after a few more splits (not shown), the process ends up splitting to 172.31.24.0/24, which is one of the original routes—meaning that 172.31.24.0/24 cannot be summarized any further in this example.

## **CIDR, Private Addresses, and NAT** 

The sky was falling in the early 1990s in that the commercialization of the Internet was rapidly depleting the IP version 4 address space. Also, Internet routers’ routing tables were doubling annually (at least). Without some changes, the incredible growth of the Internet in the 1990s would have been stifled. 

To solve the problems associated with this rapid growth, several short-term solutions were created, as well as an ultimate long-term solution. The short-term solutions included classless interdomain routing (CIDR), which helps reduce the size of routing tables by aggregating routes, and Network Address Translation (NAT), which reduces the number 

206  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

of required public IP addresses used by each organization or company. This section covers the details of CIDR and NAT, plus a few related features.

## **Classless Interdomain Routing** 

CIDR is a convention defined in RFCs 1517 through 1520 that calls for aggregating routes for multiple classful network numbers into a single routing table entry. The primary goal of CIDR is to improve the scalability of Internet routers’ routing tables. Imagine the implications of an Internet router being burdened by carrying a route to every class A, B, and C network on the planet! 

CIDR uses both technical tools and administrative strategies to reduce the size of the Internet routing tables. Technically, CIDR uses route summarization, but with Internet scale in mind. For example, CIDR might be used to allow a large ISP to control a range of IP addresses from 198.0.0.0 to 198.255.255.255, with the improvements to routing shown in  Figure  4-5 . 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0247-05.png)


**----- Start of picture text -----**<br>
Route to 198.0.0.0 Mask<br>ISP #2<br>255.0.0.0 Points to ISP #1<br>Customer #1<br>198.8.3.0/24<br>ISP #1<br>Route to 198.0.0.0 Mask  ISP #3 198.0.0.0 -<br>255.0.0.0 Points to ISP #1 198.255.255.0<br>Customer #2<br>198.4.2.0/24<br>198.4.3.0/24<br>Route to 198.0.0.0 Mask<br>ISP #4<br>255.0.0.0 Points to ISP #1<br>Customer #3<br>198.1.0.0<br>**----- End of picture text -----**<br>

## **Figure 4-5** _Typical Use of CIDR_ 

ISPs 2, 3, and 4 need only one route (198.0.0.0/8) in their routing tables to be able to forward packets to all destinations that begin with 198. Note that this summary actually summarizes multiple class C networks—a typical feature of CIDR. ISP 1’s routers contain more detailed routing entries for addresses beginning with 198, based on where they allocate IP addresses for their customers. ISP 1 would reduce its routing tables similarly with large ranges used by the other ISPs. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0247-08.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


CIDR attacks the problem of large routing tables through administrative means as well. As shown in  Figure  4-5 , ISPs are assigned contiguous blocks of addresses to use when assigning addresses for their customers. Likewise, regional authorities are assigned large address blocks, so when individual companies ask for registered public IP addresses, they ask their regional registry to assign them an address block. As a result, addresses assigned by the regional agency will at least be aggregatable into one large geographic region of the world. For example, the Latin American and Caribbean Internet Addresses Registry 

Chapter 4: IP Addressing  207 

**Key Topic** 

(LACNIC,  www.lacnic.net ) administers the IP address space of the Latin American and Caribbean region (LAC) on behalf of the Internet community. 

In some cases, the term _CIDR_ is used a little more generally than the original intent of the RFCs. Some texts use the term CIDR synonymously with the term _route summarization_ . Others use the term CIDR to refer to the process of summarizing multiple classful networks together. In other cases, when an ISP assigns subsets of a classful network to a customer who does not need an entire class C network, the ISP is essentially performing subnetting; once again, this idea sometimes gets categorized as CIDR. But CIDR itself refers to the administrative assignment of large address blocks, and the related summarized routes, for the purpose of reducing the size of the Internet routing tables. 

**Note** Because CIDR defines how to combine routes for multiple classful networks into a single route, some people think of this process as being the opposite of subnetting. As a result, many people refer to CIDR’s summarization results as _supernetting_ .

## **Private Addressing** 

One of the issues with Internet growth was the assignment of all possible network numbers to a small number of companies or organizations. Private IP addressing helps to mitigate this problem by allowing computers that will never be directly connected to the Internet to not use public, Internet-routable addresses. For IP hosts that will purposefully have no direct Internet connectivity, you can use several reserved network numbers, as defined in RFC 1918 and listed in  Table  4-12 . 

**Table 4-12** _RFC 1918 Private Address Space_ 

|**Table 4-12** _RFC 1918 Private A_|_ddress Space_||
|---|---|---|
|**Range of IP Addresses**|**Class of Networks**|**Number of Networks**|
|10.0.0.0 to 10.255.255.255|A|1|
|172.16.0.0 to 172.31.255.255|B|16|
|192.168.0.0 to 192.168.255.255|C|256|



In other words, any organization can use these network numbers. However, no organization is allowed to advertise these networks using a routing protocol on the Internet. Furthermore, all Internet routers should be configured to reject these routes.

## **Network Address Translation** 

NAT, defined in RFC 1631, enables a host that does not have a valid registered IP address to communicate with other hosts on the Internet. NAT has gained such widespread acceptance that the majority of enterprise IP networks today use private IP addresses for most 

208  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

hosts on the network and use a small block of public IP addresses, with NAT translating between the two. 

NAT translates, or changes, one or both IP addresses inside a packet as it passes through a router. (Many firewalls also perform NAT; for the CCIE Routing and Switching exam, you do not need to know NAT implementation details on firewalls.) In most cases, NAT changes the (typically private range) addresses used inside an enterprise network into addresses from the public IP address space. For example,  Figure  4-6 shows static NAT in operation; the enterprise has registered class C network 200.1.1.0/24, and uses private class A network 10.0.0.0/8 for the hosts inside its network. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0249-03.png)


**----- Start of picture text -----**<br>
SA 10.1.1.1 SA 200.1.1.1<br>Server<br>10.1.1.1<br>e0/0<br>s0/0 Internet<br>NAT<br>170.1.1.1<br>10.1.1.2<br>Inside Outside<br>DA 10.1.1.1 DA 200.1.1.1<br>Inside Local Inside Global<br>10.1.1.1 200.1.1.1<br>10.1.1.2 200.1.1.2<br>**----- End of picture text -----**<br>


**Figure 4-6** _Basic NAT Concept_ 

Beginning with the packets sent from a PC on the left to the server on the right, the private IP source address 10.1.1.1 is translated to a public IP address of 200.1.1.1. The client sends a packet with source address 10.1.1.1, but the NAT router changes the source to 200.1.1.1—a registered public IP address. When the server receives a packet with source IP address 200.1.1.1, the server thinks it is talking to host 200.1.1.1, so it replies with a packet sent to destination 200.1.1.1. The NAT router then translates the destination address (200.1.1.1) back to 10.1.1.1. 

Figure  4-6 provides a good backdrop for the introduction of a couple of key terms, _Inside Local_ and _Inside Global_ . Both terms take the perspective of the owner of the enterprise network. In  Figure  4-6 , address 10.1.1.1 is the Inside Local address, and 200.1.1.1 is the Inside Global address. Both addresses represent the client PC on the left, which is _inside the enterprise network._ Address 10.1.1.1 is from the enterprise’s IP address space, which is only _locally_ routable inside the enterprise—hence the term Inside Local. Address 200.1.1.1 represents the local host, but the address is from the globally routable public IP address space—hence the name Inside Global.  Table  4-13 lists and describes the four main NAT address terms. 

Chapter 4: IP Addressing  209 

**Key Topic** 

**Table 4-13** _NAT Terminology_ 

|**Name**|**Location of Host**|**IP Address Space in Which Address**|
|---|---|---|
||**Represented by Address**|**Exists**|
|Inside Local address|Inside the enterprise|Part of the enterprise IP address space;|
||network|typically a private IP address|
|Inside Global|Inside the enterprise|Part of the public IP address space|
|address|network||
|Outside Local|In the public Internet;|Part of the enterprise IP address space;|
|address|or, outside the enterprise|typically a private IP address|
||network||
|Outside Global|In the public Internet;|Part of the public IP address space|
|address|or, outside the enterprise||
||network||

## Static NAT 

Static NAT works just like the example in  Figure  4-6 , but with the IP addresses statically mapped to each other through configuration commands. With static NAT 

- A particular Inside Local address always maps to the same Inside Global (public) IP address. 

- If used, each Outside Local address always maps to the same Outside Global (public) IP address. 

- Static NAT does not conserve public IP addresses. 

Although static NAT does not help with IP address conservation, static NAT does allow an engineer to make an inside server host available to clients on the Internet, because the inside server will always use the same public IP address. 

Example  4-1 shows a basic static NAT configuration based on  Figure  4-6 . Conceptually, the NAT router has to identify which interfaces are inside (attach to the enterprise’s IP address space) or outside (attach to the public IP address space). Also, the mapping between each Inside Local and Inside Global IP address must be made. (Although not needed for this example, outside addresses can also be statically mapped.) 

**Example 4-1** _Static NAT Configuration_ 

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ~~! E0/0 attaches to the internal Private IP space, so it is configured as an inside ! interface.~~ **interface Ethernet0/0 ip address 10.1.1.3 255.255.255.0** 

**Key Topic** 

210  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

~~**ip nat inside** ! S0/0 is attached to the public Internet, so it is defined as an outside~~ ! interface. **interface Serial0/0 ip address 200.1.1.251 255.255.255.0** ~~**ip nat outside** ! Next, two inside addresses are mapped, with the first address stating the ! Inside Local address, and the next stating the Inside Global address.~~ ~~**ip nat inside source static 10.1.1.2 200.1.1.2 ip nat inside source static 10.1.1.1 200.1.1.1** ! Below, the NAT table lists the permanent static entries from the configuration.~~ NAT# **show ip nat translations** Pro ~~Inside global Inside local~~ Outside local      Outside global --- ~~200.1.1.1 10.1.1.1~~ ---                -- --- ~~200.1.1.2~~ 10.1.1.2           ---                --- 

The router is performing NAT only for inside addresses. As a result, the router processes packets entering E0/0—packets that could be sent by inside hosts—by examining the source IP address. Any packets with a source IP address listed in the Inside Local column of the **show ip nat translations** command output (10.1.1.1 or 10.1.1.2) will be translated to source address 200.1.1.1 or 200.1.1.2, respectively, per the NAT table. Likewise, the router examines the destination IP address of packets entering S0/0, because those packets would be destined for inside hosts. Any such packets with a destination of 200.1.1.1 or .2 will be translated to 10.1.1.1 or .2, respectively. 

In cases with static outside addresses being configured, the router also looks at the destination IP address of packets sent from the inside to the outside interfaces, and the source IP address of packets sent from outside interfaces to inside interfaces.

## Dynamic NAT Without PAT 

Dynamic NAT (without PAT), like static NAT, creates a one-to-one mapping between an Inside Local and Inside Global address. However, unlike static NAT, it does so by defining a set or pool of Inside Local and Inside Global addresses, and dynamically mapping pairs of addresses as needed. For example,  Figure  4-7 shows a pool of five Inside Global IP addresses—200.1.1.1 through 200.1.1.5. NAT has also been configured to translate any Inside Local addresses whose address starts with 10.1.1. 

Chapter 4: IP Addressing  211 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0252-01.png)


**----- Start of picture text -----**<br>
1 4<br>SA 10.1.1.2 SA 200.1.1.1<br>Inside Outside<br>Server<br>10.1.1.1<br>Internet<br>NATNAT<br>170.1.1.1<br>10.1.1.2<br>NAT Table Before First Packet<br>Criteria for Hosts to NAT: Inside Local Inside Global NAT Pool:<br>10.1.1.0 - 10.1.1.255 200.1.1.1<br>200.1.1.2<br>2 3<br>NAT Table After First Packet 200.1.1.3<br>Inside Local Inside Global 200.1.1.4<br>10.1.1.2 200.1.1.1 200.1.1.5<br>**----- End of picture text -----**<br>


**Key Topic** 

**Figure 4-7** _Dynamic NAT_ 

The numbers 1, 2, and 3 in  Figure  4-7 refer to the following sequence of events: 

**1.** Host 10.1.1.2 starts by sending its first packet to the server at 170.1.1.1. 

**2.** As the packet enters the NAT router, the router applies some matching logic to decide whether the packet should have NAT applied. Because the logic has been configured to mean “translate Inside Local addresses that start with 10.1.1,” the router dynamically adds an entry in the NAT table for 10.1.1.2 as an Inside Local address. 

**3.** The NAT router needs to allocate a corresponding IP address from the pool of valid Inside Global addresses. It picks the first one available (200.1.1.1 in this case) and adds it to the NAT table to complete the entry. 

With the completion of Step 3, the NAT router can actually translate the source IP address and forward the packet. Note that as long as the dynamic NAT entry exists in the NAT table, only host 10.1.1.2 can use Inside Global IP address 200.1.1.1.

## Overloading NAT with Port Address Translation 

As mentioned earlier, NAT is one of the key features that helped to reduce the speed at which the IPv4 address space was being depleted. _NAT overloading_ , also known as _Port Address Translation_ ( _PAT)_ , is the NAT feature that actually provides the significant savings of IP addresses. The key to understanding how PAT works is to consider the following: From a server’s perspective, there is no significant difference between 100 different TCP connections, each from a different host, and 100 different TCP connections all from the same host. 

212  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

PAT works by making large numbers of TCP or UDP flows from many Inside Local hosts appear to be the same number of large flows from one (or a few) host’s Inside Global addresses. With PAT, instead of just translating the IP address, NAT also translates the port numbers as necessary. And because the port number fields are 16 bits in length, each Inside Global IP address can support over 65,000 concurrent TCP and UDP flows. For example, in a network with 1000 hosts, a single public IP address used as the only Inside Global address could handle an average of six concurrent flows from each host to and from hosts on the Internet.

## Dynamic NAT and PAT Configuration 

Like static NAT, dynamic NAT configuration begins with identifying the inside and outside interfaces. Additionally, the set of Inside Local addresses is configured with the **ip nat inside** global command. If you are using a pool of public Inside Global addresses, the set of addresses is defined by the **ip nat pool** command.  Example  4-2 shows a dynamic NAT configuration based on the internetwork shown in  Figure  4-7 . The example defines 256 Inside Local addresses and two Inside Global addresses. 

**Example 4-2** _Dynamic NAT Configuration_ 

|**Key**|||||||
|---|---|---|---|---|---|---|
|**Topic**|||~~! First, the~~~~**ip nat pool fred **command lists a range of IP addresses. The~~~~**ip ** ~~~~**nat **~~||||
||||~~!~~~~**inside source list 1 pool**~~|~~**fred **command points to ACL 1 as the list of Inside~~|||
||||||||
||||~~! Local addresses, with a cross-reference to the pool name.~~||||
||||**interface Ethernet0/0**||||
||||**ip address 10.1.1.3 255.255.255.0**||||
||||~~**ip nat inside **~~||||
||||!||||
||||**interface Serial0/0**||||
||||**ip address 200.1.1.251 255.255.255.0**||||
||||~~**ip nat outside **~~||||
||||!||||
||||~~**ip nat pool fred 200.1.1.1 200.1.1.2 netmask 255.255.255.252 **~~||||
||||||||
||||~~**ip nat inside source list 1**~~|~~**pool fred **~~|||
||||!||||
||||~~**access-list 1 permit 10.1.1.0 0.0.0.255 **~~||||
||||||||
||||~~! Next, the NAT table begins as an empty table, because no dynamic entries had~~||||
||||||||
||||~~! been created at that point.~~||||
||||NAT#**show ip nat translations**||||
||||~~! The NAT statistics show that no hits or misses have occurred. Hits occur when~~||||
||||||||
||||~~! NAT looks for a mapping, and finds one. Misses occur when NAT looks for a NAT~~||||
||||||||
||||~~! table entry, does not find one, and then needs to dynamically add one.~~||||
||||NAT#**show ip nat statistics**||||
||||~~Total active translations:~~0 (0 static, 0 dynamic; 0 extended)||||



Chapter 4: IP Addressing  213 

Outside interfaces: Serial0/0 Inside interfaces: Ethernet0/0 ~~Hits: 0  Misses: 0~~ Expired translations: 0 Dynamic mappings: -- Inside Source access-list 1 pool fred refcount 0 pool fred: netmask 255.255.255.252 start 200.1.1.1 end 200.1.1.2 type generic, total addresses 2, allocated 0 (0%), misses 0 ~~! At this point, a Telnet session from 10.1.1.1 to 170.1.1.1 started. ! Below, the 1 "miss" means that the first packet from 10.1.1.2 did not have a ! matching entry in the table, but that packet triggered NAT to add an entry to the ! NAT table. Host 10.1.1.2 has then sent 69 more packets, noted as "hits" because ! there was an entry in the table.~~ NAT# **show ip nat statistics** Total active translations: 1 (0 static, 1 dynamic; 0 extended) Outside interfaces: Serial0/0 Inside interfaces: Ethernet0/0 ~~Hits: 69  Misses: 1~~ Expired translations: 0 Dynamic mappings: -- Inside Source access-list 1 pool fred refcount 1 pool fred: netmask 255.255.255.252 start 200.1.1.1 end 200.1.1.2 type generic, total addresses 2, allocated 1 (50%), misses 0 ! The dynamic NAT entry is now displayed in the table. NAT# **show ip nat translations** Pro Inside global      Inside local       Outside local      Outside global --- 200.1.1.1          10.1.1.2           ---                --- ~~! Below, the configuration uses PAT via the~~ ~~**overload** parameter. Could have used the !~~ ~~**ip nat inside source list 1 int s0/0 overload** command instead, using a single ! IP Inside Global IP address. NAT(config)#~~ ~~**no ip nat inside source list 1 pool fred** NAT(config)#~~ ~~**ip nat inside source list 1 pool fred overload** ! To test, the dynamic NAT entries were cleared after changing the NAT ! configuration. Before the next command was issued, host 10.1.1.1 had created two ! Telnet connections, and host 10.1.1.2 created 1 more TCP connection.~~ 

214  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

NAT# **clear ip nat translations *** NAT# **show ip nat translations** Pro Inside global      Inside local       Outside local      Outside global ~~tcp 200.1.1.1:3212     10.1.1.1:3212      170.1.1.1:23       170.1.1.1:23 tcp 200.1.1.1:3213     10.1.1.1:3213      170.1.1.1:23       170.1.1.1:23 tcp 200.1.1.1:38913    10.1.1.2:38913     170.1.1.1:23       170.1.1.1:23~~

## **IPv6** 

In the TCP/IP stack, IP is where packet sorting and delivery take place. At this layer, each incoming or outgoing packet is referred to as a _datagram_ . Each IP datagram bears the source IP address of the sender and the destination IP address of the intended recipient. Unlike MAC addresses, IP addresses in a datagram remain the same throughout a packet’s journey across an internetwork. 

As we have discussed before, the operation of IP is central to the TCP/IP stack—all other TCP/IP protocols use IP—and all data passes through it. IP is a connectionless protocol and has some limitations. If IP attempts packet delivery and in the process a packet is lost, delivered out of sequence, duplicated, or delayed, neither sender nor receiver is informed. Packet acknowledgment is handled by a higher-layer transport protocol, such as TCP, which we have discussed previously. 

IP is responsible for addressing and routing packets between hosts, and determines whether fragmentation is necessary. Fragmentation involves breaking a datagram into smaller pieces for optimized routing. The IP protocol will fragment packets prior to sending them and will also reassemble them when they reach their destination. 

The issue with IP in the modern internetwork has more to do with capacity constraints rather than operational issues. In short, we can best describe the Achilles heel of IP by pointing out the fact that the Internet has grown so significantly over the decades that there are not enough IP addresses to go around. We obviously are talking about IPv4 addresses. The version 4 address space, as discussed previously, is composed of ad - dresses defined by a series of 32 bits broken up into four separate octets through the use of “dotted decimal” notation. This means that we have a very finite number of addresses available to use at the onset, and this limitation is further compounded by the fact that many addresses in this total range have either been “reserved” for special operations or “wasted” with regard to being inefficiently issued to users. 

In short, we need another solution. That solution is the next generation IP that is being widely adopted across the globe as we speak: IPv6. IP version 6 is considered to be the best fit for the modern network because of the fact that it supports a substantially larger address space to begin with. Whereas IPv4 addresses were 32 bits long, an IPv6 address is 128 bits long. This means that the older IPv4 only supports a maximum of 2[32] IP addresses, which translates to roughly 4.29 billion total addresses. IPv6, because it utilizes 128 bits, supports a maximum of 2[128] available addresses: 

340,282,366,920,938,463,463,374,607,431,768,211,456 

Chapter 4: IP Addressing  215 

For those who care to know, that number would be read as 340 undecillion, 282 decillion, 366 nonillion, 920 octillion, 938 septillion, 463 sextillion, 463 quintillion, 374 quadrillion, 607 trillion, 431 billion, 768 million, 211 thousand, and 456. For the rest of us, we can just say it’s a very big number. 

IPv6 introduces some new concepts with regard to how we annotate addresses and how we implement and categorize address assignment.

## **IPv6 Address Format** 

IPv6 uses 16-byte hexadecimal number fields separated by colons (:) to represent the 128-bit addressing format that makes the address representation less cumbersome and error-prone. Here is an example of a valid IPv6 address:

## 2001:db8:130F:0000:0000:09C0:876A:130B 

Additionally, to shorten the IPv6 address and make the address easier to represent, IPv6 uses the following conventions: 

- Leading 0s in the address field are optional and can be compressed. 

For example: The following hexadecimal numbers can be represented as shown in a compressed format: 

   - Example 1: 0000 = 0 (compressed form) 

   - Example 2: 2001:db8:130F:0000:0000:09C0:876A:130B = 2001:db8:130F:0:0:9C0:876A:130B (compressed form) 

- A pair of colons (::) represents successive fields of 0. However, the pair of colons is allowed just once in a valid IPv6 address. 

   - Example 1: 2001:db8:130F:0:0:9C0:876A:130B = 2001:db8:130F::9C0:876A:130B (compressed form) 

   - Example 2: FF01:0:0:0:0:0:1 = FF01::1 (compressed form) 

An address parser can easily identify the number of missing 0s in an IPv6 address by separating the two parts of the address and filling in the 0s until the 128-bit address is complete. However, if two pairs of colons are placed in the same address, there is no way to identify the size of each block of 0s. The use of the :: makes many IPv6 addresses very small.

## **Network Prefix** 

In IPv6, there are references to prefixes that, in IPv4 terms, loosely equate to subnets. The IPv6 prefix is made up of the leftmost bits and acts as the network identifier. The IPv6 prefix is represented using the IPv6-prefix or prefix-length format just like an IPv4 address is represented in the classless interdomain routing (CIDR) notation. 

216  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

The / prefix-length variable is a decimal value that indicates the number of high-order contiguous bits of the address that form the prefix, which is the network portion of the address. For example, 2001:db8:8086:6502::/64 is an acceptable IPv6 prefix. If the address ends in a double colon, the trailing double colon can be omitted. So the same address can be written as 2001:db8:8086:6502/64. In either case, the prefix length is written as a decimal number 64 and represents the leftmost bits of the IPv6 address. A similar address in IPv4 would be xxx.xxx.xxx.xxx/16.

## **IPv6 Address Types** 

There is a major difference in the IP address requirements between an IPv4 host and an IPv6 host. An IPv4 host typically uses one IP address, but an IPv6 host can have more than one IP address. 

There are three major types of IPv6 addresses: 

- **Unicast:** An address for a single interface. A packet that is sent to a unicast address is delivered to the interface identified by that address. 

- **Anycast:** An address for a set of interfaces that typically belong to different nodes. A packet sent to an anycast address is delivered to the closest interface, as defined by the routing protocols in use and identified by the anycast address. 

- **Multicast:** An address for a set of interfaces (in a given scope) that typically belong to different nodes. A packet sent to a multicast address is delivered to all interfaces identified by the multicast address (in a given scope). 

Note that in the context of IPv6, there is no concept of Broadcast.

## **Address Management and Assignment** 

There are four ways to configure a host address in IPv6: 

- **Static Configuration:** Similar to IPv4, the host address, mask, and gateway address are manually defined. 

- **Stateless Address Autoconfiguration (SLAAC):** In this case, the host autonomously configures its own address. Router solicitation messages are sent by booting nodes to request Router Advertisements (RA) for configuring the interfaces (RFC 2462). 

- **Stateful DHCPv6:** The host uses Dynamic Host Configuration Protocol (DHCP) to get its IPv6 address. This addressing management is similar to IPv4 behavior (RFC 3315). 

- **Stateless DHCP:** The host uses SLAAC and also DHCP to get additional parameters such as TFTP Server, WINS, and so on. 

The configuration choice relies on Router Advertisement (RA) flags sent by the router on the LAN. The sections that follow take a cursory look at each of these methods. 

Chapter 4: IP Addressing  217

## Static Configuration 

As in IPv4, the host address can be statically defined. In this case, the IPv6 address, mask, and gateway address are all manually defined on the host. 

Static address configuration is typically used for router interface configuration but is not likely to be used for hosts in IPv6. Keep in mind that using static configuration means that all autoconfiguration features provided by IPv6 will be disabled.

## Stateless Address Autoconfiguration 

Nodes can use IPv6 Stateless Address Autoconfiguration to generate addresses without the necessity of a DHCP server. IPv6 addresses are formed by combining network prefixes with an interface identifier. On interfaces with embedded Institute of Electrical and Electronics Engineers (IEEE) identifiers, the interface identifier is typically derived from the IEEE identifier. 

The address autoconfiguration feature is built into the IPv6 protocol to facilitate intranetwide address management that enables a large number of IP hosts to easily discover the network and get new and globally unique IPv6 addresses associated with their location. The autoconfiguration feature enables plug-and-play Internet deployment of new consumer devices, such as cell phones, wireless devices, home appliances, and so on. As a result, network devices can connect to the network without manual configuration and without any servers, such as DHCP servers. We need to take a slightly closer look at the principles behind this feature. 

A router on a local link sends network-type information through RA messages, such as the prefix of the local link and the default route in its router advertisements. The router provides this information to all the nodes on the local link. 

A host can then build its address by appending a host identifier to the /64 prefix received from the router. As a result, Ethernet hosts can autoconfigure themselves by appending their 48-bit link-layer address (MAC address) in an extended universal identifier EUI-64bit format to the 64 bits of the local link prefix advertised by the router. 

Another hugely beneficial aspect to this approach is the ease with which address renumbering can be implemented. In IPv6 networks, the autoconfiguration feature makes renumbering an existing network simple and relatively easy compared to IPv4. The router sends the new prefix from the new upstream provider in its router announcements. The hosts in the network automatically pick the new prefix from the router advertisements and then use it to create their new addresses. As a result, the transition from provider A to B becomes manageable for network operators.

## Stateful DHCPv6 

Many enterprises currently use DHCP to distribute addresses to their hosts. IPv6 can be deployed with the same DHCP mechanism. 

218  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

The process for acquiring configuration data for a client in IPv6 is similar to that in IPv4. However, DHCPv6 uses multicast for many of its messages. Initially, the client must first detect the presence of routers on the link using neighbor discovery messages. If a router is found, the client examines the router advertisements to determine whether DHCP should be used. If the router advertisements enable the use of DHCP on that link (disabling the Autoconfiguration flag and enabling the Managed flag in RA messages allows a host to use DHCPv6 to obtain an IPv6 address), the client starts a DHCP solicitation phase to find a DHCP server. 

Using DHCPv6 provides the following benefits: 

- More control than serverless/stateless autoconfiguration. 

- It can be used concurrently with stateless autoconfiguration. 

- It can be used for renumbering. 

- It can be used for automatic domain name registration of hosts using dynamic DNS. 

- It can be used to delegate the IPv6 prefix to leaf customer premises equipment (CPE) routers.

## Stateless DHCP 

Stateless DHCPv6 normally combines stateless autoconfiguration for address assignment with DHCPv6 exchange for all other configuration settings. In this case, DHCPv6 is only used for the host to acquire additional parameters, such as a TFTP server, a DNS server, and so on. 

A host builds its address by appending a host identifier to the /64 prefix received from the router and then issues a DHCP solicit message to the DHCP server.

## **IPv6 Transition Technologies** 

The success of IPv6 originally was thought to depend on the new applications that run over it. However, it is becoming very clear that the exhaustion of IPv4 will ultimately end up being the driver for IPv6 adoption. A key part of any good IPv6 design is its ability to integrate into and coexist with existing IPv4 networks. IPv4 and IPv6 hosts need to coexist for a substantial length of time during the steady migration from IPv4 to IPv6, and the development of transition strategies, tools, and mechanisms has been part of the basic IPv6 design from the start. 

There are three IPv6 transition technologies: dual stack, tunneling, and translation.

## Dual Stack 

Dual stack is the basic strategy to use for large agencies that are adopting IPv6. It involves configuring devices to be able to run IPv4 and IPv6 simultaneously. IPv4 communication uses the IPv4 protocol stack, and IPv6 communication uses the IPv6 protocol stack. 

Chapter 4: IP Addressing  219 

Applications choose between using IPv4 or IPv6 based on the response to DNS requests. The application selects the correct address based on the type of IP traffic. Because dual stack allows hosts to simultaneously reach existing IPv4 content and IPv6 content as it becomes available, dual stack offers a very flexible adoption strategy. However, because IPv4 addresses are still required, dual stack is not a long-term solution to address exhaustion. 

Dual stack also avoids the need to translate between protocol stacks. Translation is a valid adoption mechanism, but it introduces operational complexity and lower performance. Because a host automatically selects the right transport to use to reach a destination based on DNS information, there should not be a need to translate between an IPv6 host and an IPv4 server.

## Tunneling 

Tunnels encapsulate IPv6 traffic within IPv4 packets, and are primarily used for communication between IPv6 (or dual stack) sites or for connection to remote IPv6 networks or hosts over an IPv4 backbone. There are many different tunneling techniques, including 6to4, ISATAP, Teredo, 6PE, 6VPE, and mGRE v6 over v4. Tunnels can be manually configured or automatically configured. Most modern operating systems include support for tunneling in addition to dual stack. 

Example  4-3 presents a simple 6to4 tunnel configuration. 

**Example 4-3** _Dynamic 6to4 Tunnel Configuration_ 

On R2 R2(config)# **int tunnel 23** R2(config-if)# **ipv6 addr 23::2/64** R2(config-if)# **tunnel source lo0** R2(config-if)# **tunnel destination 3.3.3.3** R2(config-if)# **tunnel mode ipv6ip** You should see the following console message stating that the tunnel interface is UP: 

%LINEPROTO-5-UPDOWN: Line protocol on Interface Tunnel23, changed state to up On R3 R3(config)# **int tunnel 32** R3(config-if)# **ipv6 addr 23::3/64** R3(config-if)# **tunnel source lo0** R3(config-if)# **tunnel destination 2.2.2.2** R3(config-if)# **tunnel mode ipv6ip** 

220  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

You should see the following console message stating that the tunnel interface is UP: %LINEPROTO-5-UPDOWN: Line protocol on Interface Tunnel32, changed state to up On R2 R2# **Ping 23::3** Type escape sequence to abort. Sending 5, 100-byte ICMP Echos to 23::3, timeout is 2 seconds: !!!!! Success rate is 100 percent (5/5), round-trip min/avg/max = 56/58/60 ms

## Translation 

Address Family Translation (AFT) is the process of translating addresses from one address family to another. During the adoption phase, AFT is primarily used to translate between IPv6 hosts and IPv4 content. AFT can be stateless, where reserved portions of the IPv6 address space are automatically mapped to IPv4, or it can be stateful, with addresses from a configured range used to map packets between address families. 

Nearly all enterprise deployments of IPv6 use dual stack internally. Dual stack offers a nondisruptive way to learn about and gain operational experience with a new address family, which is an important part of successfully managing the transition. 

Pilots and trials depend on specific requirements. 

Chapter 4: IP Addressing  221 

**Key Topic**

## **Foundation Summary** 

This section lists additional details and facts to round out the coverage of the topics in this chapter. Unlike most of the Cisco Press Exam Certification Guides, this “Foundation Summary” does not repeat information presented in the “Foundation Topics” section of the chapter. Please take the time to read and study the details in the “Foundation Topics” section of the chapter, as well as review items noted with a Key Topic icon. 

Table  4-14 lists and briefly explains several variations on NAT. 

**Table 4-14** _Variations on NAT_ 

|**Name**|**Function**|
|---|---|
|Static NAT|Statically correlates the same public IP address for use by the|
||same local host every time. Does not conserve IP addresses.|
|Dynamic NAT|Pools the available public IP addresses, shared among a group|
||of local hosts, but with only one local host at a time using a|
||public IP address. Does not conserve IP addresses.|
|Dynamic NAT with overload|Like dynamic NAT, but multiple local hosts share a single|
|(PAT)|public IP address by multiplexing using TCP and UDP port|
||numbers. Conserves IP addresses.|
|NAT for overlapping address|Can be done with any of the first three types. Translates both|
||source and destination addresses, instead of just the source|
||(for packets going from enterprise to the Internet).|



Table  4-15 lists the protocols mentioned in this chapter and their respective standards documents. 

**Key Topic** 

**Table 4-15** _Protocols and Standards for  Chapter  4_ 

|**Table 4-15** _Protocols and Standards for  Chapter  4_||
|---|---|
|**Name**|**Standardized In**|
|IP|RFC 791|
|Subnetting|RFC 950|
|NAT|RFC 1631|
|Private addressing|RFC 1918|
|CIDR|RFCs 1517–1520|
|DHCPv6|RFC 3315|
|Internet Protocol version 6 (IPv6) Addressing Architecture|RFC 3513|
|IPv6 Global Unicast Address Format|RFC 3587|



222  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Table  4-16 lists and describes some of the most commonly used IOS commands related to the topics in this chapter. 

**Table 4-16** _Command Reference for  Chapter  4_ 

|**Table 4-16** _Command Reference for  Chap_|_ter  4_|
|---|---|
|**Command**|**Description**|
|**ip address ** _ip-address mask_[**secondary**]|Interface subcommand to assign an IPv4|
||address|
|**ip nat **{**inside **|**outside**}|Interface subcommand; identifies inside or|
||outside part of network|
|**ip nat inside source **{**list **{_access-list-_|Global command that defines the set of inside|
|_number_|_access-list-name_} |**route-map**|addresses for which NAT will be performed,|
|_name_} {**interface ** _type number_|**pool **|and corresponding outside addresses|
|_pool-name_} [**overload**]||
|**ip nat inside destination list **{_access-list-_|Global command used with destination NAT|
|_number_|_name_}**pool ** _name_||
|**ip nat outside source **{**list **{_access-list-_|Global command used with both destination|
|_number_|_access-list-name_} |**route-map**|and dynamic NAT|
|_name_}**pool ** _pool-name_[**add-route**]||
|**ip nat pool ** _name start-ip end-ip_{**netmask**|Global command to create a pool of addresses|
|_netmask_|**prefix-length ** _prefix-length_}|for dynamic NAT|
|[**type rotary**]||
|**show ip nat statistics**|Lists counters for packets and for NAT|
||table entries, as well as basic configuration|
||information|
|**show ip nat translations **[**verbose**]|Displays the NAT table|
|**clear ip nat translation **{*** **| [**inside ** _global-ip_|Clears all or some of the dynamic entries in|
|_local-ip_] [**outside ** _local-ip global-ip_]}|the NAT table, depending on which parameters|
||are used|
|**debug ip nat**|Issues log messages describing each packet|
||whose IP address is translated with NAT|
|**show ip interface **[_type number_] [**brief**]|Lists information about IPv4 on interfaces|



Figure  4-8 shows the IP header format. 

|**Subnet ID**<br>**Interface ID**<br>**Global Routing Prefix**|**Subnet ID**<br>**Interface ID**<br>**Global Routing Prefix**|**Subnet ID**<br>**Interface ID**<br>**Global Routing Prefix**|**Subnet ID**<br>**Interface ID**<br>**Global Routing Prefix**|**Subnet ID**<br>**Interface ID**<br>**Global Routing Prefix**|
|---|---|---|---|---|
|||1st3 bytes<br>of MAC|FFFE|2nd3 bytes<br>of MAC|
|**16 bits**<br>**64 bits, EUI-64 format**<br>**48 bits**|||||
|Begins with binary 001, meaning<br>the initial hex digit is 2 or 3<br>Inverts bit 7 of MAC when<br>creating the IPv6 address|||||



**Figure 4-8** _IP Header_ 

Chapter 4: IP Addressing  223 

**Key Topic** 

Table  4-17 lists the terms and meanings of the fields inside the IP header. 

**Table 4-17** _IP Header Fields_ 

|**Field**|**Meaning**|
|---|---|
|Version|Version of the IP protocol. Most networks use IPv4 today, with IPv6|
||becoming more popular. The header format reflects IPv4.|
|Header Length|Defines the length of the IP header, including optional fields. Because|
||the length of the IP header must always be a multiple of 4, the IP header|
||length (IHL) is multiplied by 4 to give the actual number of bytes.|
|DS Field|Differentiated Services Field. This byte was originally called the Type of|
||Service (ToS) byte, but was redefined by RFC 2474 as the DS Field. It is|
||used for marking packets for the purpose of applying different quality of|
||service (QoS) levels to different packets.|
|Packet Length|Identifies the entire length of the IP packet, including the data.|
|Identification|Used by the IP packet fragmentation process. If a single packet is|
||fragmented into multiple packets, all fragments of the original packet|
||contain the same identifier so that the original packet can be reassembled.|
|Flags|3 bits used by the IP packet fragmentation process.|
|Fragment Offset|A number set in a fragment of a larger packet that identifies the fragment’s|
||location in the larger original packet.|
|Time to Live|A value used to prevent routing loops. Routers decrement this field by 1|
|(TTL)|each time the packet is forwarded; when it decrements to 0, the packet is|
||discarded.|
|Protocol|A field that identifies the contents of the data portion of the IP packet.|
||For example, protocol 6 implies that a TCP header is the first thing in the|
||IP packet data field.|
|Header|A value used to store a frame check sequence (FCS) value, whose purpose|
|Checksum|is to determine whether any bit errors occurred in the IP header (not the|
||data) during transmission.|
|Source IP|The 32-bit IP address of the sender of the packet.|
|Address||
|Destination IP|The 32-bit IP address of the intended recipient of the packet.|
|Address||
|Optional Header|IP supports additional header fields for future expansion through optional|
|Fields and|headers. Also, if these optional headers do not use a multiple of 4 bytes,|
|Padding|padding bytes are added, composed of all binary 0s, so that the header is|
||a multiple of 4 bytes in length.|



Table  4-18 lists some of the more common IP protocol field values. 

224  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 4-18** _IP Protocol Field Values_ 

||**Table 4-18** _IP Protocol Field Values_|
|---|---|
|**Key**<br>**Topic**||
||**Protocol Name**<br>**Protocol Number**|
||ICMP<br>1|
||TCP<br>6|
||UDP<br>17|
||EIGRP<br>88|
||OSPF<br>89|
||PIM<br>103|



Figure  4-9 Illustrates an IPv6 header. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0265-04.png)


**----- Start of picture text -----**<br>
Version ToS<br>Len ID Offset TTL Proto FCS IP SA IP DA Data<br>Length Byte<br>IPv4 Packet<br>7 6 5 4 3 2 1 0<br>IP Precedence Unused Standard IPv4<br>DiffServ Code Point (DSCP) Flow Ctrl DiffServ Extensions<br>Figure 4-9  IPv6 Header<br> Table  4-19 lists the terms and meanings for the fields in the header illustration.<br>Table 4-19  IPv6 Header Fields<br> Field   Meaning<br> Version   4 bits. IPv6 version number.<br> Traffic Class   8 bits. Internet traffic priority delivery value.<br> Flow Label   20 bits. Used for specifying special router handling from the source<br>to the destination(s) for a sequence of packets.<br> Payload Length   16 bits. Specifies the length of the data in the packet. When cleared<br>to 0, the option is a hop-by-hop Jumbo payload.<br> Next Header   8 bits. Specifies the next encapsulated protocol. The values are<br>compatible with those specified for the IPv4 protocol field.<br> Hop Limit   8 bits. For each router that forwards the packet, the hop limit is<br>decremented by 1. When the hop limit field reaches 0, the packet is<br>discarded. This replaces the TTL field in the IPv4 header that was<br>originally intended to be used as a time-based hop limit.<br> Source Address   16 bytes. The IPv6 address of the sending node.<br> Destination Address   16 bytes. The IPv6 address of the destination node.<br>**----- End of picture text -----**<br>


Chapter 4: IP Addressing  225

## **Memory Builders** 

The CCIE Routing and Switching written exam, like all Cisco CCIE written exams, covers a fairly broad set of topics. This section provides some basic tools to help you exercise your memory about some of the broader topics covered in this chapter.

## **Fill in Key Tables from Memory** 

Appendix  E , “Key Tables for CCIE Study,” on the CD in the back of this book, contains empty sets of some of the key summary tables in each chapter. Print  Appendix  E , refer to this chapter’s tables in it, and fill in the tables from memory. Refer to  Appendix  F , “Solutions for Key Tables for CCIE Study,” on the CD to check your answers.

## **Definitions** 

Next, take a few moments to write the definitions for the following terms: 

subnet, prefix, classless IP addressing, classful IP addressing, CIDR, NAT, IPv4, subnet broadcast address, subnet number, subnet zero, broadcast subnet, subnet mask, private addresses, SLSM, VLSM, Inside Local address, Inside Global address, Outside Local address, Outside Global address, PAT, overloading, quartet, IPv6, 6to4 Tunnel, ISATAP, DHCPv6, AFT 

Refer to the glossary to check your answers.

## **Further Reading** 

All topics in this chapter are covered in varying depth for the CCNP Routing exam. For more details on these topics, look for the CCNP routing study guides at www.ciscopress.com/ccnp . 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0267-00.png)

## **Blueprint topics covered in this chapter:** 

This chapter covers the following subtopics from the Cisco CCIE Routing and Switching written exam blueprint. Refer to the full blueprint in Table I-1 in the Introduction for more details on the topics covered in each chapter and their context within the blueprint. 

- Hot Standby Router Protocol (HSRP) 

- Gateway Load Balancing Protocol (GLBP) 

- Virtual Router Redundancy Protocol (VRRP) 

- Dynamic Host Configuration Protocol (DHCP) 

- Network Time Protocol (NTP) 

- Web Cache Communication Protocol (WCCP) 

- Network Management 

- Logging and Syslog 

- Troubleshoot Network Services 

- Implement IP Service Level Agreement (IP SLA) 

- Object Tracking 

- Implement NetFlow 

- Implement Router IP Traffic Export (RITE) 

- Implement SNMP 

- Implement Cisco IOS Embedded Event Manager (EEM) 

- Implement Remote Monitoring (RMON) 

- Implement FTP 

- Implement TFTP 

- Implement TFTP Server on Router 

- Implement Secure Copy Protocol (SCP) 

- Implement HTTP and HTTPS 

- Implement Telnet 

- Implement SSH

## **CHAPTER 5**

## **IP Services** 

IP relies on several protocols to perform a variety of tasks related to the process of routing packets. This chapter provides a reference for the most popular of these protocols. In addition, this chapter covers a number of management-related protocols and other blueprint topics related to IP services.

## **“Do I Know This Already?” Quiz** 

Table  5-1 outlines the major headings in this chapter and the corresponding “Do I Know This Already?” quiz questions. 

**Table 5-1** _“Do I Know This Already?” Foundation Topics Section-to-Question Mapping_ 

|**Table 5-1** _“Do I Know This Already?” Foundation_|_Topics Section-to-Question_|_Mappin_|
|---|---|---|
|**Foundation Topics Section**|**Questions Covered in**|**Score**|
||**This Section**||
|ARP, Proxy ARP, Reverse ARP, BOOTP, and DHCP|1–3||
|HSRP, VRRP, and GLBP|4–6||
|Network Time Protocol|7||
|SNMP|8–9||
|Web Cache Communication Protocol|10–11||
|Implement SSH|12||
|Implement SSH, HTTPS, FTP, SCP, TFTP|13||
|Implement RMON|14||
|Implement IP SLA, NetFlow, RITE, EEM|15||
|**Total Score**|||



228  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

To best use this pre-chapter assessment, remember to score yourself strictly. You can find the answers in  Appendix  A , “Answers to the ‘Do I Know This Already?’ Quizzes.” 

**1.** Two hosts, named PC1 and PC2, sit on subnet 172.16.1.0/24, along with Router R1. A web server sits on subnet 172.16.2.0/24, which is connected to another interface of R1. At some point, both PC1 and PC2 send an ARP request before they successfully send packets to the web server. With PC1, R1 makes a normal ARP reply, but for PC2, R1 uses a proxy ARP reply. Which two of the following answers could be true given the stated behavior in this network? 

   - **a.** PC2 set the proxy flag in the ARP request. 

   - **b.** PC2 encapsulated the ARP request inside an IP packet. 

   - **c.** PC2’s ARP broadcast implied that PC2 was looking for the web server’s MAC address. 

   - **d.** PC2 has a subnet mask of 255.255.0.0. 

   - **e.** R1’s proxy ARP reply contains the web server’s MAC address. 

**2.** Host PC3 is using DHCP to discover its IP address. Only one router attaches to PC3’s subnet, using its fa0/0 interface, with an **ip helper-address 10.5.5.5** command on that same interface. That same router interface has an **ip address 10.4.5.6 255.255.252.0** command configured as well. Which of the following are true about PC3’s DHCP request? 

   - **a.** The destination IP address of the DHCP request packet is set to 10.5.5.5 by the router. 

   - **b.** The DHCP request packet’s source IP address is unchanged by the router. 

   - **c.** The DHCP request is encapsulated inside a new IP packet, with source IP address 10.4.5.6 and destination 10.5.5.5. 

   - **d.** The DHCP request’s source IP address is changed to 10.4.5.255. 

   - **e.** The DHCP request’s source IP address is changed to 10.4.7.255. 

**3.** Which of the following statements are true about BOOTP, but not true about RARP? 

   - **a.** The client can be assigned a different IP address on different occasions, because the server can allocate a pool of IP addresses for allocation to a set of clients. 

   - **b.** The server can be on a different subnet from the client. 

   - **c.** The client’s MAC address must be configured on the server, with a one-to-one mapping to the IP address to be assigned to the client with that MAC address. 

   - **d.** The client can discover its IP address, subnet mask, and default gateway IP address. 

Chapter 5: IP Services  229 

**4.** R1 is HSRP active for virtual IP address 172.16.1.1, with HSRP priority set to 115. R1 is tracking three separate interfaces. An engineer configures the same HSRP group on R2, also connected to the same subnet, only using the **standby 1 ip 172.16.1.1** command, and no other HSRP-related commands. Which of the following would cause R2 to take over as HSRP active? 

   - **a.** R1 experiences failures on tracked interfaces, totaling 16 or more lost points. 

   - **b.** R1 experiences failures on tracked interfaces, totaling 15 or more lost points. 

   - **c.** R2 could configure a priority of 116 or greater. 

   - **d.** R1’s fa0/0 interface fails. 

   - **e.** R2 would take over immediately. 

**5.** Which Cisco IOS feature does HSRP, GLBP, and VRRP use to determine when an interface fails for active switching purposes? 

   - **a.** Each protocol has a built-in method of tracking interfaces. 

   - **b.** When a physical interface goes down, the redundancy protocol uses this automatically as a basis for switching. 

   - **c.** Each protocol uses its own hello mechanism for determining which interfaces are up or down. 

   - **d.** The Cisco IOS object tracking feature. 

**6.** Which is the correct term for using more than one HSRP group to provide load balancing for HSRP? 

   - **a.** LBHSRP 

   - **b.** LSHSRP 

   - **c.** RHSRP 

   - **d.** MHSRP 

   - **e.** None of these is correct. HSRP does not support load balancing. 

**7.** Which of the following NTP modes in a Cisco router requires a predefinition of the IP address of an NTP server? 

   - **a.** Server mode 

   - **b.** Static client mode 

   - **c.** Broadcast client mode 

   - **d.** Symmetric active mode 

230  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**8.** Which of the following are true about SNMP security? 

   - **a.** SNMP Version 1 calls for the use of community strings that are passed as clear text. 

   - **b.** SNMP Version 2c calls for the use of community strings that are passed as MD5 message digests generated with private keys. 

   - **c.** SNMP Version 3 allows for authentication using MD5 message digests generated with private keys. 

   - **d.** SNMP Version 3 authentication also requires concurrent use of encryption, typically done with DES. 

**9.** Which of the following statements are true regarding features of SNMP based on the SNMP version? 

   - **a.** SNMP Version 2 added the GetNext protocol message to SNMP. 

   - **b.** SNMP Version 3 added the Inform protocol message to SNMP. 

   - **c.** SNMP Version 2 added the Inform protocol message to SNMP. 

   - **d.** SNMP Version 3 expanded the SNMP Response protocol message so that it must be used by managers in response to Traps sent by agents. 

   - **e.** SNMP Version 3 enhanced SNMP Version 2 security features but not other features. 

**10.** WCCP uses what protocol and port for communication between content engines and WCCP routers? 

   - **a.** UDP 2048 

   - **b.** TCP 2048 

   - **c.** UDP 4082 

   - **d.** TCP 4082 

**11.** In a WCCP cluster, which content engine becomes the lead engine after the cluster stabilizes? 

   - **a.** The content engine with the lowest IP address. 

   - **b.** The content engine with the highest IP address. 

   - **c.** There is no such thing as a lead content engine; the correct term is designated content engine. 

   - **d.** All content engines have equal precedence for redundancy and the fastest possible load sharing. 

Chapter 5: IP Services  231 

**12.** Which configuration commands are required to enable SSH on a router? 

   - **a. hostname** 

   - **b. ip domain-name** 

   - **c. ip ssh** 

   - **d. crypto key generate rsa** 

   - **e. http secure-server** 

**13.** Which protocol is the most secure choice, natively, for transferring files from a router? 

   - **a.** SSH 

   - **b.** HTTPS 

   - **c.** FTP 

   - **d.** TFTP 

   - **e.** SCP 

**14.** In RMON, which type of configured option includes rising and falling thresholds, either relative or absolute, and is monitored by another type of RMON option? 

   - **a.** Event 

   - **b.** Alert 

   - **c.** Notification 

   - **d.** Port 

   - **e.** Probe 

**15.** Which Cisco IOS feature permits end-to-end network performance monitoring with configuration on devices at each end of the network? 

   - **a.** Flexible NetFlow 

   - **b.** IP SLA 

   - **c.** EEM 

   - **d.** RITE 

232  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Foundation Topics**

## **ARP, Proxy ARP, Reverse ARP, BOOTP, and DHCP** 

The heading for this section might seem like a laundry list of a lot of different protocols. However, these five protocols do have one central theme, namely, that they help a host learn information so that it can successfully send and receive IP packets. Specifically, Address Resolution Protocol (ARP) and proxy ARP define methods for a host to learn another host’s MAC address, whereas the core functions of Reverse ARP (RARP), Bootstrap Protocol (BOOTP), and DHCP define how a host can discover its own IP address, plus additional related information.

## **ARP and Proxy ARP** 

You would imagine that anyone getting this far in his CCIE study would already have a solid understanding of the Address Resolution Protocol (ARP, RFC 826). However, proxy ARP (RFC 1027) is often ignored, in part because of its lack of use today. To see how they both work,  Figure  5-1 shows an example of each, with Fred and Barney both trying to reach the web server at IP address 10.1.2.200. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0273-06.png)


**----- Start of picture text -----**<br>
ARP Request<br>Fred: 10.1.1.101 Target = 10.1.1.1<br>Mask: /24<br>GW = 10.1.1.1<br>ARP Reply<br>Source = R1-E1-MAC Web Server:<br>Interface: E1 10.1.2.200/24<br>MAC: R1-E1-MAC GW = 10.1.2.1<br>10.1.1.1/24<br>R1 DHCP Server:<br>Interface: E2 10.1.2.202/24<br>MAC: R1-E2-MAC<br>10.1.2.1/24<br>ARP Request<br>Barney: 10.1.1.102 Target = 10.1.2.200 DNS Server:10.1.2.203/24<br>Mask: /8<br>GW = 10.1.1.1 ARP Reply Proxy logic<br>Source = R1-E1-MAC used by R1!<br>**----- End of picture text -----**<br>


**Figure 5-1** _Comparing ARP and Proxy ARP_ 

Fred follows a normal ARP process, broadcasting an ARP request, with R1’s E1 IP address as the target. The ARP message has a _Target_ field of all 0s for the MAC address that needs to be learned, and a target IP address of the IP address whose MAC address it is searching, namely, 10.1.1.1 in this case. The ARP reply lists the MAC address associated with the IP address, in this case, the MAC address of R1’s E1 interface. 

Chapter 5: IP Services  233 

**Note** The ARP message itself does not include an IP header, although it does have destination and source IP addresses in the same relative position as an IP header. The ARP request lists an IP destination of 255.255.255.255. The ARP Ethernet protocol type is 0x0806, whereas IP packets have an Ethernet protocol type of 0x0800. 

Proxy ARP uses the exact same ARP message as ARP, but the ARP request is actually requesting a MAC address that is not on the local subnet. Because the ARP request is broadcast on the local subnet, it will not be heard by the target host—so if a router can route packets to that target host, the router issues a proxy ARP reply on behalf of that target. 

For example, Barney places the web server’s IP address (10.1.2.200) in the Target field, because Barney thinks that he is on the same subnet as the web server because of Barney’s mask of 255.0.0.0. The ARP request is a LAN broadcast, so R1, being a wellbehaved router, does not forward the ARP broadcast. However, knowing that the ARP request will never get to the subnet where 10.1.2.200 resides, R1 saves the day by replying to the ARP on behalf of the web server. R1 takes the web server’s place in the ARP process, hence the name _proxy_ ARP. Also, note that R1’s ARP reply contains R1’s E1 MAC address, so that Barney will forward frames to R1 when Barney wants to send a packet to the web server. 

Before the advent of DHCP, many networks relied on proxy ARP, configuring hosts to use the default masks in their respective networks. Regardless of whether the proxy version is used, the end result is that the host learns a router’s MAC address to forward packets to another subnet.

## **RARP, BOOTP, and DHCP** 

The ARP and proxy ARP processes both occur after a host knows its IP address and subnet mask. RARP, BOOTP, and DHCP represent the evolution of protocols defined to help a host dynamically learn its IP address. All three protocols require the client host to send a broadcast to begin discovery, and all three rely on a server to hear the request and supply an IP address to the client.  Figure  5-2 shows the basic processes with RARP and BOOTP. 

A RARP request is a host’s attempt to find its own IP address. So RARP uses the same old ARP message, but the ARP request lists a MAC address target of its own MAC address and a target IP address of 0.0.0.0. A preconfigured RARP server, which must be on the same subnet as the client, receives the request and performs a table lookup in its configuration. If that target MAC address listed in the ARP request is configured on the RARP server, the RARP server sends an ARP reply, after entering the configured IP address in the Source IP address field. 

234  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0275-01.png)


**----- Start of picture text -----**<br>
RARP Configuration<br>Key Topic 1 RARP Broadcast Hannah RARP Server MAC  IP<br>0200.1111.1111   10.1.1.1<br>2 RARP Reply 0200.1234.5678   10.1.1.2<br>IP: ?.?.?.?<br>1 0200.5432.1111   10.1.1.3<br>MAC: 0200.1111.1111<br>2<br>Hey Everybody! My MAC Address Is Your IP Address Is<br>0200.1111.1111. If You Are a RARP<br>10.1.1.1<br>Server, Please Tell Me My IP Address!<br>BOOTP Configuration<br>Hannah MAC  IP  Gateway<br>1 BOOTP Broadcast  BOOTP Server  0200.1111.1111 10.1.1.1    10.1.1.200<br>2 BOOTP Reply 0200.1234.5678 10.1.1.2 10.1.1.200<br>IP: ?.?.?.? 0200.5432.1111  10.1.1.3 10.1.1.200<br>1<br>MAC: 0200.1111.1111<br>2 10.1.1.200<br>Hey Everybody! My MAC Address Is Your IP Address Is 10.1.1.1<br>0200.1111.1111. If You Are a BOOTP<br>Server, Please Tell Me My IP Address! Your Default Gateway Is 10.1.1.200… R1<br>**----- End of picture text -----**<br>


**Figure 5-2** _RARP and BOOTP—Basic Processes_ 

BOOTP was defined in part to improve IP address assignment features of RARP. BOOTP **Key** uses a completely different set of messages, defined by RFC 951, with the commands **Topic** encapsulated inside an IP and UDP header. With the correct router configuration, a router can forward the BOOTP packets to other subnets—allowing the deployment of a centrally located BOOTP server. Also, BOOTP supports the assignment of many other tidbits of information, including the subnet mask, default gateway, DNS addresses, and its namesake, the IP address of a boot (or image) server. However, BOOTP does not solve the configuration burden of RARP, still requiring that the server be preconfigured with the MAC addresses and IP addresses of each client.

## **DHCP** 

DHCP represents the next step in the evolution of dynamic IP address assignment. Building on the format of BOOTP protocols, DHCP focuses on dynamically assigning a variety of information and provides flexible messaging to allow for future changes, without requiring predefinition of MAC addresses for each client. DHCP also includes temporary leasing of IP addresses, enabling address reclamation, pooling of IP addresses, and, recently, dynamic registration of client Domain Name System (DNS) fully qualified domain names (FQDN). (See  www.ietf.org for more information on FQDN registration.) 

DHCP servers typically reside in a centralized location, with remote routers forwarding the LAN-broadcast DHCP requests to the DHCP server by changing the request’s destination address to match the DHCP server. This feature is called DHCP relay agent. For example, in  Figure  5-1 , if Fred and Barney were to use DHCP, with the DHCP server at 10.1.2.202, R1 would change Fred’s DHCP request from a destination of 255.255.255.255 to a destination of 10.1.2.202. R1 would also list its own IP address in the message, in the gateway IP address (giaddr) field, notifying the DHCP server of the IP address to which 

Chapter 5: IP Services  235 

the response should be sent. After receiving the next DHCP message from the server, R1 would change the destination IP address to a LAN broadcast, and forward the packet onto the client’s LAN. The only configuration requirement on the router is an **ip helperaddress 10.1.2.202** interface subcommand on its E1 interface. 

Alternatively, R1 could be configured as a DHCP server—a feature that is not often configured on routers in production networks but is certainly fair game for the CCIE written and lab exams. Configuring DHCP on a router consists of several required steps: 

**Step 1.** Configure a DHCP pool. 

**Step 2.** Configure the router to exclude its own IP address from the DHCP pool. 

**Step 3.** Disable DHCP conflict logging or configure a DHCP database agent. 

The DHCP pool includes key items such as the subnet (using the **network** command within DHCP pool configuration), default gateway ( _default-router_ ), and the length of time for which the DHCP lease is valid ( _lease_ ). Other items, including the DNS domain name and any DHCP options, are also defined within the DHCP pool. 

Although not strictly necessary in DHCP configuration, it is certainly a best practice to configure the router to make its own IP address in the DHCP pool subnet unavailable for allocation through DHCP. The same is true for any other static IP addresses within the DHCP pool range, such as those of servers and other routers. Exclude host IP addresses from the DHCP process using the **ip dhcp excluded-address** command. 

**Note** The **ip dhcp excluded-address** command is one of the relatively few Cisco IOS **ip** commands that is a global configuration command rather than an interface command. 

The Cisco IOS DHCP server also provides a mechanism for logging DHCP address conflicts to a central server called a DHCP database agent. IOS requires that you either disable conflict logging by using the **no ip dhcp conflict-logging** command or configure a DHCP database agent on a server by using the **ip dhcp database** command.  Example  5-1 shows R1’s configuration for a DHCP relay agent, as well as an alternative for R1 to provide DNS services for subnet 10.1.1.0/24. 

**Example 5-1** _DHCP Configuration Options—R1,  Figure  5-1_ 

~~! UDP broadcasts coming in E0 will be forwarded as unicasts to 10.1.2.202. ! The source IP will be changed to 10.1.1.255, so that the reply packets will be~~ 

~~! broadcast back out E0.~~ **interface Ethernet1** ip address 10.1.1.1 255.255.255.0 ~~**ip helper-address 10.1.2.202**~~ 

~~! Below, an alternative configuration, with R1 as the DHCP server. R1 assigns IP ! addresses other than the excluded first 20 IP addresses in the subnet, and~~ 

~~! informs the clients of their IP addresses, mask, DNS, and default router. Leases~~ 

236  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

~~! are for 0 days, 0 hours, and 20 minutes.~~ **ip dhcp excluded-address 10.1.1.0 10.1.1.20** ! **ip dhcp pool subnet1 network 10.1.1.0 255.255.255.0 dns-server 10.1.2.203 default-router 10.1.1.1 lease 0 0 20** 

Table  5-2 summarizes some of the key comparison points with RARP, BOOTP, and DHCP. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0277-03.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


**Table 5-2** _Comparing RARP, BOOTP, and DHCP_ 

|**Feature**|**RARP**|**BOOTP**|**DHCP**|
|---|---|---|---|
|Relies on server to allocate IP addresses|Yes|Yes|Yes|
|Encapsulates messages inside IP and UDP so that they can be|No|Yes|Yes|
|forwarded to a remote server||||
|Client can discover its own mask, gateway, DNS, and|No|Yes|Yes|
|download server||||
|Dynamic address assignment from a pool of IP addresses,|No|No|Yes|
|without requiring knowledge of client MACs||||
|Allows temporary lease of IP address|No|No|Yes|
|Includes extensions for registering client’s FQDN with a DNS|No|No|Yes|

## **HSRP, VRRP, and GLBP** 

IP hosts can use several methods of deciding which default router or default gateway to use—DHCP, BOOTP, ICMP Router Discovery Protocol (IRDP), manual configuration, or even by running a routing protocol (although having hosts run a routing protocol is not common today). The most typical methods—using DHCP or manual configuration—result in the host knowing a single IP address of its default gateway. Hot Standby Router Protocol (HSRP), Virtual Router Redundancy Protocol (VRRP), and Gateway Load Balancing Protocol (GLBP) represent a chronological list of some of the best tools for overcoming the issues related to a host knowing a single IP address as its path to get outside the subnet. 

Chapter 5: IP Services  237 

**Key Topic** 

HSRP allows multiple routers to share a virtual IP and MAC address so that the end-user hosts do not realize when a failure occurs. Some of the key HSRP features are as follows: 

- Virtual IP address and virtual MAC are active on the HSRP Active router. 

- Standby routers listen for Hellos from the Active router, defaulting to a 3-second hello interval and 10-second dead interval. 

- Highest priority (IOS default 100, range 1–255) determines the Active router, with preemption disabled by default. 

- Supports tracking, whereby a router’s priority is decreased when a tracked object (interface or route) fails. 

- Up to 255 HSRP groups per interface, enabling an administrative form of load balancing. 

- Virtual MAC of 0000.0C07.ACxx, where xx is the hex HSRP group. 

- Virtual IP address must be in the same subnet as the routers’ interfaces on the same LAN. 

- Virtual IP address must be different from any of the routers’ individual interface IP addresses. 

- Supports clear-text and MD5 authentication (through a key chain). 

Example  5-2 shows a typical HSRP configuration, with two groups configured. Routers R1 and R2 are attached to the same subnet, 10.1.1.0/24, both with WAN links (S0/0.1) connecting them to the rest of an enterprise network. Cisco IOS provides the tracking mechanism shown in  Example  5-2 to permit many processes, including HSRP, VRRP, and GLBP, to track interface states. A tracking object can track based on the line protocol (shown here) or the IP routing table. The example contains the details and explanation of the configuration. 

**Example 5-2** _HSRP Configuration_ 

~~! First, on Router R1, a tracking object must be configured so that ! HSRP can track the interface state.~~ **track 13 interface Serial0/0.1 line-protocol** ~~! Next, on Router R1, two HSRP groups are configured. R1 has a higher priority ! in group 21, with R2 having a higher priority in group 22. R1 is set to preempt ! in group 21, as well as to track interface s0/0.1 for both groups.~~ **interface FastEthernet0/0 ip address 10.1.1.1 255.255.255.0 standby 21 ip 10.1.1.21** continues **standby 21 priority 105 standby 21 preempt standby 21 track 13 standby 22 ip 10.1.1.22** 

**Key Topic** 

238  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**standby 22 track 13** 

~~! Next, R2 is configured with a higher priority for HSRP group 22, and with ! HSRP tracking enabled in both groups. The tracking "decrement" used by R2, ! when S0/0.1 fails, is set to 9 (instead of the default of 10). ! A tracking object must be configured first, as on R1.~~ track 23 interface Serial0/0.1 line-protocol **interface FastEthernet0/0 ip address 10.1.1.2 255.255.255.0 standby 21 ip 10.1.1.21 standby 21 track 23 standby 22 ip 10.1.1.22 standby 22 priority 105 standby 22 track 23 decrement 9** !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ~~! On R1 below, for group 21, the output shows that R1 is active, with R2 ! (10.1.1.2) as standby. ! R1 is tracking s0/0.1, with a default "decrement" of 10, meaning that the ! configured priority of 105 will be decremented by 10 if s0/0.1 fails.~~ Router1# **sh standby fa0/0** FastEthernet0/0 - Group 21 ~~State is Active~~ 2 state changes, last state change 00:00:45 Virtual IP address is 10.1.1.21 Active virtual MAC address is 0000.0c07.ac15 Local virtual MAC address is 0000.0c07.ac15 (v1 default) Hello time 3 sec, hold time 10 sec Next hello sent in 2.900 secs Preemption enabled Active router is local Standby router is 10.1.1.2, priority 100 (expires in 7.897 sec) Priority 105 (configured 105) Track object 13 state Up decrement 10 IP redundancy name is "hsrp-Fa0/0-21" (default) ! output omitted ~~! NOT SHOWN—R1 shuts down S0.0.1, lowering its priority in group 21 by 10. ! The~~ ~~**debug** below shows the reduced priority value. However, R2 does not become ! active, because R2's configuration did not include a~~ ~~**standby 21 preempt** command. Router1#~~ ~~**debug standby**~~ *Mar  1 00:24:04.122: HSRP: Fa0/0 Grp 21 Hello  out 10.1.1.1 Active  pri 95 vIP 10.1.1.21 

Chapter 5: IP Services  239 

**Key Topic** 

Because HSRP uses only one Active router at a time, any other HSRP routers are idle. To provide load sharing in an HSRP configuration, the concept of Multiple HSRP, or MHSRP, was developed. In MHSRP, two or more HSRP groups are configured on each HSRP LAN interface, where the configured priority determines which router will be active for each HSRP group. 

MHSRP requires that each DHCP client and statically configured host are issued a default gateway corresponding to one of the HSRP groups and requires that they’re distributed appropriately. Thus, in an MHSRP configuration with two routers and two groups, all other things being equal, half of the hosts should have one HSRP group address as its default gateway, and the other half of the hosts should use the other HSRP group address. If you now revisit  Example  5-2 , you will see that it is an MHSRP configuration. 

HSRP is Cisco proprietary, has been out a long time, and is widely popular. VRRP (RFC 3768) provides a standardized protocol to perform almost the exact same function. The Cisco VRRP implementation has the same goals in mind as HSRP but with these differences: 

**Key Topic** 

- VRRP uses a multicast virtual MAC address (0000.5E00.01 _xx_ , where _xx_ is the hex VRRP group number). 

- VRRP uses the IOS object tracking feature, rather than its own internal tracking mechanism, to track interface states for failover purposes. 

- VRRP defaults to use preemption, but HSRP defaults to not use preemption. Both can be configured to either use preemption or not. 

- The VRRP term _Master_ means the same thing as the HSRP term _Active_ . 

- In VRRP, the VRRP group IP address is the interface IP address of one of the VRRP routers. 

GLBP is a newer Cisco-proprietary tool that adds load-balancing features in addition to gateway-redundancy features. Hosts still point to a default gateway IP address, but GLBP causes different hosts to send their traffic to one of up to four routers in a GLBP group. To do so, the GLBP Active Virtual Gateway (AVG) assigns each router in the group a unique virtual MAC address, following the format 0007.B400. _xxyy_ , where _xx_ is the GLBP group number and _yy_ is a different number for each router (01, 02, 03, or 04). When a client ARPs for the (virtual) IP address of its default gateway, the GLBP AVG replies with one of the four possible virtual MACs. By replying to ARP requests with different virtual MACs, the hosts in that subnet will in effect balance the traffic across the routers, rather than send all traffic to the one active router. 

Cisco IOS devices with GLBP support permit configuring up to 1024 GLBP groups per physical interface and up to four hosts per GLBP group. 

240  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Network Time Protocol** 

NTP Version 3 (RFC 1305) allows IP hosts to synchronize their time-of-day clocks with a common source clock. For example, routers and switches can synchronize their clocks to make event correlation from an SNMP management station more meaningful, by ensuring that any events and traps have accurate time stamps. 

By design, most routers and switches use NTP _client mode_ , adjusting their clocks based on the time as known by an NTP server. NTP defines the messages that flow between client and server, and the algorithms a client uses to adjust its clock. Routers and switches can also be configured as NTP servers, as well as using NTP _symmetric active mode_ —a mode in which the router or switch mutually synchronizes with another NTP host. 

NTP servers can reference other NTP servers to obtain a more accurate clock source as defined by the _stratum level_ of the ultimate source clock. For example, atomic clocks and Global Positioning System (GPS) satellite transmissions provide a source of stratum 1 (lowest/best possible stratum level). For an enterprise network, the routers and switches can refer to a low-stratum NTP source on the Internet, or purpose-built rack-mounted NTP servers, with built-in GPS capabilities, can be deployed. 

Example  5-3 shows a sample NTP configuration on four routers, all sharing the same 10.1.1.0/24 Ethernet subnet. Router R1 will be configured as an NTP server. R2 acts as an _NTP static client_ by virtue of the static configuration referencing R1’s IP address. R3 acts as an _NTP broadcast client_ by listening for R1’s NTP broadcasts on the Ethernet. Finally, R4 acts in NTP symmetric active mode, configured with the **ntp peer** command. 

**Example 5-3** _NTP Configuration_ 

**Key Topic** !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ~~! First, R1's configuration, the~~ ~~**ntp broadcast** command under interface fa0/0 ! causes NTP to broadcast NTP updates on that interface. The first three of the ! four global NTP commands configure authentication; these commands are identical ! on all the routers.~~ R1# **show running-config** interface FastEthernet0/0 ~~ntp broadcast~~ ! ntp authentication-key 1 md5 1514190900 7 ntp authenticate ntp trusted-key 1 ~~ntp master 7 ! Below, the "127.127.7.1" notation implies that this router is the NTP clock ! source. The clock is synchronized, with stratum level 7, as configured on the !~~ ~~**ntp master 7** command above.~~ R1# **show ntp associations** 

Chapter 5: IP Services  241 

address         ref clock     st  when  poll reach  delay  offset    disp *~127.127.7.1      127.127.7.1       6    22    64  377     0.0    0.00     0.0 * master (synced), # master (unsynced), + selected, - candidate, ~ configured R1# **show ntp status** Clock is synchronized, stratum 7, reference is 127.127.7.1 nominal freq is 249.5901 Hz, actual freq is 249.5901 Hz, precision is 2**16 reference time is C54483CC.E26EE853 (13:49:00.884 UTC Tue Nov 16 2004) clock offset is 0.0000 msec, root delay is 0.00 msec root dispersion is 0.02 msec, peer dispersion is 0.02 msec ~~! R2 is configured below as an NTP static client. Note that the~~ ~~**ntp clock-period** ! command is automatically generated as part of the synchronization process, and ! should not be added to the configuration manually.~~ R2# **show run | begin ntp** ntp authentication-key 1 md5 1514190900 7 ntp authenticate ntp trusted-key 1 ntp clock-period 17208144 ~~ntp server 10.1.1.1~~ end ~~! Next, R3 has been configured as an NTP broadcast client. The~~ ~~**ntp broadcast client** ! command on R3 tells it to listen for the broadcasts from R1. This configuration ! relies on the~~ ~~**ntp broadcast** subcommand on R1's Fa0/0 interface, as shown at the ! beginning of this example.~~ R3# **show run** interface Ethernet0/0 ~~ntp broadcast client ! R4's configuration is listed, with the~~ ~~**ntp peer** ! command implying the use of symmetric active mode.~~ R4# **show run | beg ntp** ntp authentication-key 1 md5 0002010300 7 ntp authenticate ntp trusted-key 1 ntp clock-period 17208233 ~~ntp peer 10.1.1.1~~

## **SNMP** 

This section of the chapter summarizes some of the core Simple Network Management Protocol (SNMP) concepts and details, particularly with regard to features of different SNMP versions. SNMP or, more formally, the _Internet Standard Management Framework_ , uses a structure in which the device being managed (the SNMP agent) has information that the management software (the SNMP manager) wants to display to someone operating the network. Each SNMP agent keeps a database, called 

242  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

a _Management Information Base (MIB)_ , that holds a large variety of data about the operation of the device on which the agent resides. The manager collects the data by using SNMP. 

SNMP has been defined with four major functional areas to support the core function of allowing managers to manage agents: 

- **Data Definition:** The syntax conventions for how to define the data to an agent or manager. These specifications are called the _Structure of Management Information (SMI)_ . 

- **MIBs:** More than 100 Internet standards define different MIBs, each for a different technology area, with countless vendor-proprietary MIBs as well. The MIB definitions conform to the appropriate SMI version. 

- **Protocols:** The messages used by agents and managers to exchange management data. 

- **Security and Administration:** Definitions for how to secure the exchange of data between agents and managers. 

Interestingly, by separating SNMP into these major functional areas, each part has been improved and expanded independently over the years. However, it is important to know a few of the main features added for each official SNMP version, as well as for a pseudoversion called SNMPv2c, as summarized in  Table  5-3 . 

**Table 5-3** _SNMP Version Summaries_ 

|**Key**|||
|---|---|---|
|**Topic**|**SNMP**|**Description**|
||**Version**||
||1|Uses SMIv1, simple authentication with communities, but used MIB-I originally.|
||2|Uses SMIv2, removed requirement for communities, added GetBulk and Inform|
|||messages, but began with MIB-II originally.|
||2c|Pseudo-release (RFC 1905) that allowed SNMPv1-style communities with|
|||SNMPv2; otherwise, equivalent to SNMPv2.|
||3|Mostly identical to SNMPv2, but adds significantly better security, although it|
|||supports communities for backward compatibility. Uses MIB-II.|



Table  5-3 hits the highlights of the comparison points between the various SNMP versions. As you might expect, each release builds on the previous one. For example, SNMPv1 defined _community strings_ for use as simple clear-text passwords. SNMPv2 removed the requirement for community strings—however, backward compatibility for SNMP communities was defined through an optional RFC (1901). Even SNMPv3, with much better security, supports communities to allow backward compatibility. 

Chapter 5: IP Services  243 

**Note** The use of SNMPv1 communities with SNMPv2, based on RFC 1901, has popularly been called _SNMP Version 2c_ , with _c_ referring to “communities,” although it is arguably not a legitimate full version of SNMP. 

The next few sections provide a bit more depth about the SNMP protocol, with additional details about some of the version differences.

## **SNMP Protocol Messages** 

The SNMPv1 and SNMPv2 protocol messages (RFC 3416) define how a manager and agent, or even two managers, can communicate information. For example, a manager can use three different messages to get MIB variable data from agents, with an SNMP _Response_ message returned by the agent to the manager supplying the MIB data. SNMP uses UDP exclusively for transport, using the SNMP Response message to both acknowledge receipt of other protocol messages and supply SNMP information. 

Table  5-4 summarizes the key information about each of the SNMP protocol messages, including the SNMP version in which the message first appeared. 

**Key Topic** 

**Table 5-4** _SNMP Protocol Messages (RFCs 1157 and 1905)_ 

|**Message**|**Initial**|**Response**|**Typically**|**Main Purpose**|
|---|---|---|---|---|
||**Version**|**Message**|**Sent By**||
|Get|1|Response|Manager|A request for a single variable’s value.|
|GetNext|1|Response|Manager|A request for the next single MIB leaf|
|||||variable in the MIB tree.|
|GetBulk|2|Response|Manager|A request for multiple consecutive MIB|
|||||variables with one request. Useful for getting|
|||||complex structures, for example, an IP|
|||||routing table.|
|Response|1|None|Agent|Used to respond with the information in Get|
|||||and Set requests.|
|Set|1|Response|Manager|Sent by a manager to an agent to tell the|
|||||agent to set a variable to a particular value.|
|||||The agent replies with a Response message.|
|Trap|1|None|Agent|Allows agents to send unsolicited|
|||||information to an SNMP manager. The|
|||||manager does not reply with any SNMP|
|||||message.|
|Inform|2|Response|Manager|A message used between SNMP managers to|
|||||allow MIB data to be exchanged.|



244  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

The three variations of the SNMP Get message, and the SNMP Response message, are typically used when someone is actively using an SNMP manager. When a user of the SNMP manager asks for information, the manager sends one of the three types of Get commands to the agent. The agent replies with an SNMP Response message. The different variations of the Get command are useful, particularly when the manager wants to view large portions of the MIB. An agent’s entire MIB—whose structure can vary from agent to agent—can be discovered with successive GetNext requests, or with GetBulk requests, using a process called a _MIB walk_ . 

The SNMP Set command allows the manager to change something on the agent. For example, the user of the management software can specify that a router interface should be shut down; the management station can then issue a Set command for a MIB variable on the agent. The agent sets the variable, which tells Cisco IOS Software to shut down the interface. 

SNMP Traps are unsolicited messages sent by the agent to the management station. For example, when an interface fails, a router’s SNMP agent could send a Trap to the SNMP manager. The management software could then highlight the failure information on a screen, email first-level support personnel, page support, and so on. Also of note, there is no specific message in response to the receipt of a Trap; technically, of the messages in  Table  5-4 , only the Trap and Response messages do not expect to receive any kind of acknowledging message. 

Finally, the Inform message allows two SNMP managers to exchange MIB information about agents that they both manage.

## **SNMP MIBs** 

SNMP Versions 1 and 2 included a standard generic MIB, with initial MIB-I (version 1, RFC 1156) and MIB-II (version 2, RFC 1213). MIB-II was actually created in between the release of SNMPv1 and v2, with SNMPv1 supporting MIB-II as well. After the creation of the MIB-II specification, the IETF SNMP working group changed the strategy for MIB definition. Instead of the SNMP working group creating standard MIBs, other working groups, in many different technology areas, were tasked with creating MIB definitions for their respective technologies. As a result, hundreds of standardized MIBs are defined. Additionally, vendors create their own vendor-proprietary MIBs. 

The Remote Monitoring MIB (RMON, RFC 2819) is a particularly important standardized MIB outside MIB-II. An SNMP agent that supports the RMON MIB can be programmed, through SNMP Set commands, to capture packets, calculate statistics, monitor thresholds for specific MIB variables, report back to the management station when thresholds are reached, and perform other tasks. With RMON, a network can be populated with a number of monitoring probes, with SNMP messaging used to gather the information as needed. 

Chapter 5: IP Services  245

## **SNMP Security** 

SNMPv3 added solid security to the existing SNMPv2 and SNMPv2c specifications. SNMPv3 adds two main branches of security to SNMPv2: authentication and encryption. SNMPv3 specifies the use of message digest algorithm 5 (MD5) and secure hash algorithm (SHA) to create a message digest for each SNMPv3 protocol message. Doing so enables authentication of endpoints and prevents data modification and masquerade types of attacks. Additionally, SNMPv3 managers and agents can use Digital Encryption Standard (DES) to encrypt the messages, providing better privacy. (SNMPv3 suggests future support of Advanced Encryption Standard [AES] as well, but that is not a part of the original SNMPv3 specifications.) The encryption feature remains separate because of the U.S. government export restrictions on DES technology. 

Example  5-4 shows a typical SNMP configuration with the following goals: 

- Enable SNMP and send traps to 192.168.1.100. 

- Send traps for a variety of events to the SNMP manager. 

- Set optional information to identify the router chassis, contact information, and location. 

- Set read-write access to the router from the 192.168.1.0/24 subnet (filtered by access list 33). 

**Example 5-4** _Configuring SNMP_ 

access-list 33 permit 192.168.1.0 0.0.0.255 snmp-server community public RW 33 snmp-server location B1 snmp-server contact routerhelpdesk@mail.local snmp-server chassis-id 2511_AccessServer_Canadice snmp-server enable traps snmp snmp-server enable traps hsrp snmp-server enable traps config snmp-server enable traps entity snmp-server enable traps bgp snmp-server enable traps rsvp snmp-server enable traps frame-relay snmp-server enable traps rtr snmp-server host 192.168.1.100 public

## **Syslog** 

Event logging is nothing new to most CCIE candidates. Routers and switches, among other devices, maintain event logs that reveal a great deal about the operating conditions of that device, along with valuable time-stamp information to help troubleshoot problems or chains of events that take place. 

246  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

By default, Cisco routers and switches do not log events to nonvolatile memory. They can be configured to do so using the **logging buffered** command, with an additional argument to specify the size of the log buffer. Configuring a router, for example, for SNMP management provides a means of passing critical events from the event log, as they occur, to a network management station in the form of traps. SNMP is, however, fairly involved to configure. Furthermore, if it’s not secured properly, SNMP also opens attack vectors to the device. However, disabling SNMP and watching event logs manually is at best tedious, and this approach simply does not scale. 

Syslog, described in RFC 5424, is a lightweight event-notification protocol that provides a middle ground between manually monitoring event logs and a full-blown SNMP implementation. It provides real-time event notification by sending messages that enter the event log to a Syslog server that you specify. Syslog uses UDP port 514 by default. 

Cisco IOS devices configured for Syslog, by default, send all events that enter the event log to the Syslog server. You can also configure Syslog to send only specific classes of events to the server. 

Syslog is a clear-text protocol that provides event notifications without requiring difficult, time-intensive configuration or opening attack vectors. In fact, it’s quite simple to configure basic Syslog operation: 

- **Step 1.** Install a Syslog server on a workstation with a fixed IP address. 

- **Step 2.** Configure the logging process to send events to the Syslog server’s IP address using the **logging host** command. 

- **Step 3.** Configure any options, such as which severity levels (0–7) you want to send to the Syslog server using the **logging trap** command.

## **Web Cache Communication Protocol** 

To ease pressure on congested WAN links in networks with many hosts, Cisco developed WCCP to coordinate the work of edge routers and content engines (also known as cache engines). Content engines collect frequently accessed data, usually HTTP traffic, locally, so that when hosts access the same pages, the content can be delivered from the cache engine rather than crossing the WAN. WCCP differs from web proxy operation in that the hosts accessing the content have no knowledge that the content engine is involved in a given transaction. 

WCCP works by allowing edge routers to communicate with content engines to make each aware of the other’s presence and to permit the router to redirect traffic to the content engine as appropriate.  Figure  5-3 shows how WCCP functions between a router and a content engine when a user requests a web object using HTTP. 

Chapter 5: IP Services  247 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0288-01.png)


**----- Start of picture text -----**<br>
ARP Request<br>Key  Fred: 10.1.1.101Mask: /24 Target = 10.1.1.1<br>Topic GW = 10.1.1.1<br>ARP Reply<br>Source = R1-E1-MAC Web Server:<br>Interface: E1 10.1.2.200/24<br>MAC: R1-E1-MAC GW = 10.1.2.1<br>10.1.1.1/24<br>R1 DHCP Server:<br>Interface: E2 10.1.2.202/24<br>MAC: R1-E2-MAC<br>10.1.2.1/24<br>ARP Request<br>Barney: 10.1.1.102 Target = 10.1.2.200 DNS Server:10.1.2.203/24<br>Mask: /8<br>GW = 10.1.1.1 ARP Reply Proxy logic<br>Source = R1-E1-MAC used by R1!<br>**----- End of picture text -----**<br>


**Figure 5-3** _WCCP Operations Between a Router and a Content Engine_ 

The figure shows the following steps, with the main decision point on the content engine coming at Step 4: 

- **Step 1.** The client sends an HTTP Get request with a destination address of the web server, as normal. 

- **Step 2.** The router’s WCCP function notices the HTTP Get request and redirects the packet to the content engine. 

- **Step 3.** The content engine looks at its disk storage cache to discover whether the requested object is cached. 

- **Step 4A.** If the object is cached, the content engine sends an HTTP response, which includes the object, back to the client. 

- **Step. 4B** If the object is not cached, the content engine sends the original HTTP Get request on to the original server. 

- **Step 5.** If Step 4B was taken, the server replies to the client, with no knowledge that the packet was ever redirected to a content engine. 

Using WCCP, which uses UDP port 2048, a router and a content engine, or a pool of content engines (known as a cluster), become aware of each other. In a cluster of content engines, the content engines also communicate with each other using WCCP. Up to 32 content engines can communicate with a single router using WCCPv1. If more than one content engine is present, the one with the lowest IP address is elected as the lead engine. 

WCCP also provides a means for content engines within a cluster to become aware of each other. Content engines request information on the cluster members from the WCCP router, which replies with a list. This permits the lead content engine to determine how traffic should be distributed to the cluster. 

In WCCPv1, only one router can redirect traffic to a content engine or a cluster of content engines. In WCCPv2, multiple routers and multiple content engines can be configured as a WCCP service group. This expansion permits much better scalability in content caching. Furthermore, WCCPv1 supports only HTTP traffic (TCP port 80,  specifically). 

**Key Topic** 

248  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

WCCPv2 supports several other traffic types and has other benefits compared to WCCPv1: 

- Supports TCP and UDP traffic other than TCP port 80, including FTP caching, FTP 

- **Key** proxy handling, web caching for ports other than 80, Real Audio, video, and tele- 

- **Topic** phony. 

   - Permits segmenting caching services provided by a caching cluster to a particular protocol or protocols, and uses a priority system for deciding which cluster to use for a particular cached protocol. 

   - Supports multicast to simplify configuration. 

   - Supports multiple routers (up to 32 per cluster) for redundancy and load distribution. (All content engines in a cluster must be configured to communicate with all routers in that cluster.) 

   - Provides for MD5 security in WCCP communication using the global configuration command **ip wccp password** _password_ . 

   - Provides load distribution. 

   - Supports transparent error handling. 

When you enable WCCP globally on a router, the default version used is WCCPv2. Because the WCCP version is configured globally for a router, the version number affects all interfaces. However, multiple services can run on a router at the same time. Routers and content engines can also simultaneously participate in more than one service group. These WCCP settings are configured on a per-interface basis. 

Configuring WCCP on a router is not difficult because a lot of the configuration in a caching scenario takes place on the content engines; the routers need only minimal configuration.  Example  5-5 shows a WCCPv2 configuration using MD5 authentication and multicast for WCCP communication. 

**Example 5-5** _WCCP Configuration Example_ 

**Key Topic** ~~! First we enable WCCP globally on the router, ! specifying a service (web caching), a multicast address for ! the WCCP communication, and an MD5 password:~~ **ip wccp web-cache group-address 239.128.1.100 password cisco** ~~! Next we configure an interface to redirect WCCP web-cache ! traffic outbound to a content engine:~~ **int fa0/0 ip wccp web-cache redirect out** ~~! Finally, inbound traffic on interface fa0/1 is excluded from redirection:~~ **int fa0/1 ip wccp redirect exclude in** 

Chapter 5: IP Services  249 

Finally, WCCP can make use of access lists to filter traffic only for certain clients (or to exclude WCCP use for certain clients) using the **ip wccp web-cache redirect-list** _accesslist_ global command. WCCP can also use ACLs to determine which types of redirected traffic the router should accept from content engines, using the global command **ip wccp web-cache group-list** _access-list_ .

## **Implementing the Cisco IOS IP Service Level Agreement (IP SLA) Feature** 

The Cisco IOS IP SLA feature, formerly known as the Service Assurance Agent (SAA), and prior to that simply the Response Time Reporter (RTR) feature, is designed to provide a means of actively probing a network to gather performance information from it. Whereas most of the tools described in the following sections are designed to monitor and collect information, IP SLA is based on the concept of generating traffic at a specified interval, with specifically configured options, and measuring the results. It is built around a source-responder model, where one device (the source) generates traffic and either waits for a response from another device (the responder) or another device configured as a responder captures the sender’s traffic and does something with it. This model provides the ability to analyze actual network performance over time, under very specific conditions, to measure performance, avert outages, evaluate quality of service (QoS) performance, identify problems, verify SLAs, and reduce network outages. The IP SLA feature is extensively documented at  www.cisco.com/go/ipsla . 

The IP SLA feature allows measuring the following parameters in network performance: 

- Delay (one-way and round-trip) 

- Jitter (directional) 

- Packet loss (directional) 

- Packet sequencing 

- Path (per hop) 

- Connectivity (through the UDP Echo, ICMP Echo, ICMP Path Echo, and TCP Connect functions) 

- Server or website download time 

- Voice-quality metrics (MOS) 

Implementing the IP SLA feature requires these steps: 

- **Step 1.** Configure the SLA operation type, including any required options. 

- **Step 2.** Configure any desired threshold conditions. 

- **Step 3.** Configure the responder(s), if appropriate. 

250  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

- **Step 4.** Schedule or start the operation and monitor the results for a sufficient period of time to meet your requirements. 

**Step 5.** Review and interpret the results. You can use the Cisco IOS CLI or an SNMP manager to do this. 

After IP SLA monitors have been configured, they cannot be edited or modified. You must delete an existing IP SLA monitor to reconfigure any of its options. Also, when you delete an IP SLA monitor to reconfigure it, the associated schedule for that IP SLA monitor is deleted, too. 

IP SLAs can use MD5 authentication. These are configured using the **ip sla key-chain** command. 

Example  5-6 shows a basic IP SLA configuration with the UDP Echo function. On the responding router, the only required command is global config **ip sla monitor responder** . On the originating router, the configuration shown in the example sets the source router to send UDP echo packets every 5 seconds for one day to 200.1.200.9 on port 1330. 

**Example 5-6** _IP SLA Basic Configuration_ 

SLAdemo# **config term** SLAdemo(config)# **ip sla monitor 1** SLAdemo(config-sla-monitor)# **type udpEcho dest-ipaddr 200.1.200.9 dest-port 1330** SLAdemo(config-sla-monitor)# **frequency 5** SLAdemo(config-sla-monitor)# **exit** SLAdemo(config)# **ip sla monitor schedule 1 life 86400 start-time now** 

A number of **show** commands come in handy in verifying IP SLA performance. On the source router, the most useful commands are **show ip sla monitor statistics** and **show ip sla monitor configuration** . Here’s a sample of the **show ip sla monitor statistics** command for the sending router in the configuration in  Example  5-6 : 

SLAdemo# **show ip sla monitor statistics** Round trip time (RTT)   Index 1 Latest RTT: 26 ms Latest operation start time: 19:42:44.799 EDT Tue Jun 9 2009 Latest operation return code: OK Number of successes: 228 Number of failures: 0 Operation time to live: 78863 sec

## **Implementing NetFlow** 

NetFlow is a software feature set in Cisco IOS that is designed to provide network administrators information about what is happening in the network, so that those responsible for the network can make appropriate design and configuration changes and monitor for network attacks. NetFlow has been included in Cisco IOS for a long time, and 

Chapter 5: IP Services  251 

has evolved through several versions (currently version 9). Cisco has renamed the feature Cisco Flexible NetFlow. It is more than just a renaming, however. The original NetFlow implementation included a fixed seven tuples that identified a flow. Flexible NetFlow allows a user to configure the number of tuples to more specifically target a particular flow to monitor. 

The components of NetFlow are 

- **Records:** A set of predefined and user-defined key fields (such as source IP address, destination IP address, source port, and so on) for network monitoring. 

- **Flow monitors:** Applied to an interface, flow monitors include records, a cache, and optionally a flow exporter. The flow monitor cache collects information about flows. 

- **Flow exporters:** These export the cached flow information to outside systems (typically a server running a NetFlow collector). 

- **Flow samplers:** Designed to reduce the load on NetFlow-enabled devices, flow samplers allow specifying the sample size of traffic, NetFlow analyzes to a ratio of 1:2 through 1:32768 packets. That is, the number of packets analyzed is configurable from 1/2 to 1/32768 of the packets flowing across the interface. 

Configuring NetFlow in its most basic form uses predefined flow records, configured for collection by a flow monitor, and at least one flow exporter.  Example  5-7 shows a basic NetFlow configuration for collecting information and statistics on IPv4 traffic using the predefined IPv4 record, and for configuring some timer settings to show their structure. An exporter is configured to send the collected information to a server at 192.168.1.110 on UDP port 1333, and with a Differentiated Services Code Point (DSCP) of 8 on the exported packets. The process consists of three steps: configuring the NetFlow monitor, applying it to an interface, and configuring an exporter. 

**Example 5-7** _Basic NetFlow Monitor and Exporter Configuration_ 

EastEdge# **show run | begin flow** flow exporter ipv4flowexport destination 192.168.1.110 dscp 8 transport udp 1333 ! flow monitor ipv4flow description Monitors all IPv4 traffic record netflow ipv4 original-input cache timeout inactive 600 cache timeout active 180 cache entries 5000 statistics packet protocol ! 

252  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

interface FastEthernet0/0 ip address 192.168.39.9 255.255.255.0 ip flow monitor ipv4flow input ! output omitted 

You can verify NetFlow configuration using these commands: 

- **show flow record** 

- **show flow monitor** 

- **show flow exporter** 

- **show flow interface**

## **Implementing Router IP Traffic Export** 

IP Traffic Export, or Router IP Traffic Export (RITE), exports IP packets to a VLAN or LAN interface for analysis. RITE does this only for traffic received on multiple WAN or LAN interfaces simultaneously as would typically take place only if the device were being targeted in a denial of service attack. The primary application for RITE is in intrusion detection system (IDS) implementations, where duplicated traffic can indicate an attack on the network or device. In case of actual attacks where identical traffic is received simultaneously on multiple ports of a router, it’s useful to have the router send that traffic to an IDS for alerting and analysis—that’s what RITE does. 

When configuring RITE, you enable it and configure it to direct copied packets to the MAC address of the IDS host or protocol analyzer. You can configure forwarding of inbound traffic (the default), outbound traffic, or both, and filtering on the number of packets forwarded. Filtering can be performed with access lists and based on one-in- _n_ packets. 

In  Example  5-8 , a router is configured with a RITE profile that’s applied to the fa0/0 interface and exports traffic to a host with the MAC address 0018.0fad.df30. The router is configured for bidirectional RITE, and to send one in every 20 inbound packets and one in every 100 outbound packets to this MAC address. The egress interface (toward the IDS host) is fa0/1. For simplicity,  Example  5-8 shows only one ingress interface. Configuration for other ingress interfaces uses the same steps shown here for the fa0/0 interface. 

**Example 5-8** _Router IP Traffic Export Example_ 

Edge# **config term** Edge(config)# **ip traffic-export profile export-this** Edge(config-rite)# **interface fa0/0** Edge(config-rite)# **bidirectional** Edge(config-rite)# **mac-address 0018.0fad.df30** Edge(config-rite)# **incoming sample one-in-every 20** Edge(config-rite)# **outgoing sample one-in-every 100** 

Chapter 5: IP Services  253 

Edge(config-rite)# **exit** Edge(config)# **interface fa0/1** Edge(config-if)# **ip traffic-export apply export-this** Edge(config-if)# **end** Edge# %RITE-5-ACTIVATE: Activated IP traffic export on interface FastEthernet 0/1.

## **Implementing Cisco IOS Embedded Event Manager** 

The Embedded Event Manager is a software component of Cisco IOS that is designed to make life easier for administrators by tracking and classifying events that take place on a router and providing notification options for those events. The Cisco motivation for including EEM was to reduce downtime, thus improving availability, by reducing the mean time to recover from various system events that previously required a manual troubleshooting and remediation process. 

In some ways, EEM overlaps with RMON functionality, but EEM is considerably more powerful and flexible. EEM uses _event detectors_ and _actions_ to provide notifications of those events. Event detectors that EEM supports include the following: 

- Monitoring SNMP objects 

- Screening Syslog messages for a pattern match (using regular expressions) 

- Monitoring counters 

- Timers (absolute time-of-day, countdown, watchdog, and CRON) 

- Screening CLI input for a regular expression match 

- Hardware insertion and removal 

- Routing table changes 

- IP SLA and NetFlow events 

- Generic On-Line Diagnostics (GOLD) events 

- Many others, including redundant switchover events, inbound SNMP messages, and others 

Event actions that EEM provides include the following: 

- Generating prioritized Syslog messages 

- Reloading the router 

- Switching to a secondary processor in a redundant platform 

- Generating SNMP traps 

254  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

- Setting or modifying a counter 

- Executing a Cisco IOS command 

- Sending a brief email message 

- Requesting system information when an event occurs 

- Reading or setting the state of a tracked object 

EEM policies can be written using either the Cisco IOS CLI or using the Tcl command interpreter language. For the purposes of the CCIE Routing and Switching qualification exam, you’re more likely to encounter CLI-related configuration than Tcl, but both are very well documented at  www.cisco.com/go/eem .  Example  5-9 is a brief example configuration that shows the CLI configuration of an EEM event that detects and then sends a notification that a console user has issued the **wr** command, as well as the associated console output when the command is issued. 

**Example 5-9** _EEM Configuration Example_ 

R9(config)# **event manager applet CLI-cp-run-st** R9(config-applet)# **event cli pattern "wr" sync yes** R9(config-applet)# **action 1.0 syslog msg "$_cli_msg Command Executed"** R9(config-applet)# **set 2.0 _exit_status 1** R9(config-applet)# **end** R9# **wr** Jun  9 19:23:21.989: %HA_EM-6-LOG: CLI-cp-run-st: write Command Executed 

The Cisco IOS EEM has such vast capability that an entire book on the subject is easily conceivable, but considering the scope of the CCIE Routing and Switching qualifying exam, these fundamental concepts should provide you with enough working knowledge to interpret questions you might encounter.

## **Implementing Remote Monitoring** 

Remote Monitoring, or RMON, is an event-notification extension of the SNMP capability on a Cisco router or switch. RMON enables you to configure thresholds for alerting based on SNMP objects, so that you can monitor device performance and take appropriate action to any deviations from the normal range of performance indications. 

RMON is divided into two classes: alarms and events. An event is a numbered, userconfigured threshold for a particular SNMP object. You configure events to track, for example, CPU utilization or errors on a particular interface, or anything else you can do with an SNMP object. You set the rising and falling thresholds for these events, and then tell RMON which RMON alarm to trigger when those rising or falling thresholds are crossed. For example, you might want to have the router watch CPU utilization and trigger an SNMP trap or log an event when the CPU utilization rises faster than, say, 20 percent per minute. Or you might configure it to trigger an alarm when the CPU utilization rises to some absolute level, such as 80 percent. Both types of thresholds (relative, or 

Chapter 5: IP Services  255 

“delta,” and absolute) are supported. Then, you can configure a different alarm notification as the CPU utilization falls, again at some delta or to an absolute level you specify. 

The alarm that corresponds to each event is also configurable in terms of what it does (logs the event or sends a trap). If you configure an RMON alarm to send a trap, you also need to supply the SNMP community string for the SNMP server. 

Event and alarm numbering are locally significant. Alarm numbering provides a pointer to the corresponding event. That is, the configured events each point to specific alarm numbers, which you must also define. 

Example  5-10 shows the configuration required to identify two pairs of events, and the four corresponding alarm notifications. The events being monitored are the interface error counter on the FastEthernet 0/0 interface (SNMP object ifInErrors.1) and the Serial 0/0 interface (SNMP object ifInErrors.2). In the first case, the RMON event looks for a delta (relative) rise in interface errors in a 60-second period, and a falling threshold of five errors per 60 seconds. In the second case, the numbers are different and the thresholds are absolute, but the idea is the same. In each case, the RMON events drive RMON alarms 1, 2, 3, or 4, depending on which threshold is crossed. 

**Example 5-10** _RMON Configuration Example_ 

rmon event 1 log trap public description Fa0.0RisingErrors owner config rmon event 2 log trap public description Fa0.0FallingErrors owner config rmon event 3 log trap public description Se0.0RisingErrors owner config rmon event 4 log trap public description Se0.0FallingErrors owner config rmon alarm 11 ifInErrors.1 60 delta rising-threshold 10 1 falling-threshold 5 2 owner config 

rmon alarm 20 ifInErrors.2 60 absolute rising-threshold 20 3 falling-threshold 10 4 owner   config 

To monitor RMON activity and to see the configured alarms and events, use the **show rmon alarm** and **show rmon event** commands. Here’s an example of the console events that take place when the previously configured events trigger the corresponding alarms: 

Jun  9 12:54:14.787: %RMON-5-FALLINGTRAP: Falling trap is generated because the value   of ifInErrors.1 has fallen below the fallingthreshold value 5 

Jun  9 12:55:40.732: %RMON-5-FALLINGTRAP: Falling trap is generated because the value   of ifInErrors.2 has fallen below the fallingthreshold value 10

## **Implementing and Using FTP on a Router** 

You can use the Cisco IOS FTP client to send or receive files from the CLI. Cisco IOS does not support configuration as an FTP server, but you can configure a TFTP server (see the next section of this chapter for details). 

256  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

To transfer files using FTP from the CLI, use the **ip ftp** command with the appropriate options. You can specify the username and password to use for an FTP transfer using the **ip ftp username** and **ip ftp password** commands. You can also specify the source interface used for FTP transfers using the **ip ftp** _source-interface_ command. 

To initiate an FTP transfer, use the **copy** command with the **ftp** keyword in either the source or destination argument. For example, to send the startup configuration file on a router to an FTP server at 10.10.200.1, where it will be stored as r8-startup-config, the transaction is shown in  Example  5-11 . 

**Example 5-11** _Using FTP to Copy a Configuration File_ 

R8# **copy startup-config ftp:** Address or name of remote host []? **10.10.200.1** Destination filename [r8-confg]? **r8-startup-config** Writing r8-startup-config  ! 3525 bytes copied in 0.732 secs 

FTP can also be used to send an exception dump to an FTP server in the event of a crash. Example  5-12 shows a router configured to send an exception dump of 65,536 bytes to 172.30.19.63 using the username JoeAdmin and password c1sco. 

**Example 5-12** _Using FTP to Send an Exception Dump_ 

ip ftp username JoeAdmin ip ftp password c1sco ! exception protocol ftp exception region-size 65536 exception dump 172.30.19.63 

Finally, you can set the router for passive-mode FTP connections by configuring the **ip ftp passive** command.

## **Implementing a TFTP Server on a Router** 

TFTP is commonly used for IOS and configuration file transfers on routers and switches. Cisco IOS supports configuring a TFTP server on a router, and the process is straightforward. It should be noted that TFTP is a tool that allows files to be “pulled” from one device to another. 

To enable TFTP, issue the **tftp-server** command, which has several arguments. You can specify the memory region where the file resides (typically flash, but other regions are supported), the filename, and an access list for controlling which hosts can access the 

Chapter 5: IP Services  257 

file. Here’s an example that shows the commands to permit TFTP access to flash:c1700advipservicesk9-mz.124-23.bin to hosts that are identified by access list 11. This example also shows how the alias command-line option can be used to make the file available with a name other than the one that it has natively in flash, specifically supersecretfile.bin: 

tftp-server flash:c1700-advipservicesk9-mz.124-23.bin alias supersecretfile.bin 11

## **Implementing Secure Copy Protocol** 

Secure Copy Protocol (SCP) is a service you can enable on a Cisco IOS router or switch to provide file copy services. SCP uses Secure Shell (SSH) (TCP port 22) for its transport protocol. It enables file transfer using the IOS **copy** command. 

SCP requires authentication, authorization, and accounting (AAA) for user authentication and authorization. Therefore, you must enable AAA before turning on SCP. In particular, because **copy** is an exec command, you must configure the **aaa authorization** command with the **exec** option. After you’ve enabled AAA, use the **ip scp server enable** command to turn on the SCP server.

## **Implementing HTTP and HTTPS Access** 

Cisco IOS routers and switches support web access for administration, through both HTTP and HTTPS. Enabling HTTP access requires the **ip http server** global configuration command. HTTP access defaults to TCP port 80. You can change the port used for HTTP by configuring the **ip http port** command. You can restrict HTTP access to a router using the **ip http access-class** command, which applies an extended access list to connection requests. You can also specify a unique username and password for HTTP access using the **ip http client username** and **ip http client password** commands. If you choose, you can also configure HTTP access to use a variety of other access-control methods, including AAA, using **ip http authentication** [ **aaa** | **local** | **enable** | **tacacs** ]. 

You can also configure a Cisco IOS router or switch for Secure Sockets Layer (SSL) access. By default, HTTPS uses TCP port 443, and the port is configurable in much the same way as it is with HTTP access. Enabling HTTPS access requires the **ip http secureserver** command. When you configure HTTPS access in most IOS Release 12.4 versions, the router or switch automatically disables HTTP access, if it has been configured. However, you should disable it manually if the router does not do it for you. 

HTTPS router access also gives you the option of specifying the cipher suite of your choice. This is the combination of encryption methods that the router will enable for HTTPS access. By default, all methods are enabled, as shown in the sample **show** _command_ output of  Example  5-13 . 

258  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Example 5-13** _HTTPS Configuration Output on a Router_ 

R8# **sh ip http server secure status** HTTP secure server status: Enabled HTTP secure server port: 443 HTTP secure server ciphersuite: 3des-ede-cbc-sha des-cbc-sha rc4-128-md5 rc4-128-sha HTTP secure server client authentication: Disabled HTTP secure server trustpoint: HTTP secure server active session modules: ALL R8#

## **Implementing Telnet Access** 

Telnet is such a ubiquitous method of access on Cisco IOS routers and switches that it needs little coverage here. Still, a few basic points are in order. 

Telnet requires a few configuration specifics to work. On the vty lines, the **login** command (or a variation of it such as **login local** ) must be configured. If a **login** command is not configured, the router or switch will refuse all Telnet connection attempts. 

By default, Telnet uses TCP port 23. However, you can configure the vty lines to use rotary groups, also known as rotaries, to open access on other ports. If you configure this option, you should use an extended access list to enforce connection on the desired ports. By default, rotaries support connections on a number of ports. For example, if you configure **rotary 33** on the vty lines, the router will accept Telnet connections on ports 3033, 5033, and 7033. Therefore, filtering undesired ports is prudent. Remember that applying access lists to vty lines requires the **access-class** _list_ **in** command.

## **Implementing SSH Access** 

Secure Shell (SSH) is much more secure than Telnet because it uses SSL rather than clear text. Therefore, today, nearly all Cisco router and switch deployments use SSH rather than Telnet for secure access. Enabling SSH on a Cisco router is a four-step process. This is because SSH requires a couple of items to be configured before you can enable SSH itself, and those prerequisites are not intuitive. The steps in configuring SSH are as follows: 

**Step 1.** Configure a host name using the **hostname** command. **Step 2.** Configure a domain name using the **ip domain-name** command. **Step 3.** Configure RSA keys using the **crypto key generate rsa** command. **Step 4.** Configure the terminal lines to permit SSH access using the **transport input ssh** command. 

SSH supports rotaries on vty lines just as Telnet does, so you can use rotaries to specify the port or ports on which SSH access is permitted on vty lines. 

Chapter 5: IP Services  259 

**Key Topic**

## **Foundation Summary** 

This section lists additional details and facts to round out the coverage of the topics in this chapter. Unlike most of the Cisco Press Exam Certification Guides, this “Foundation Summary” does not repeat information presented in the “Foundation Topics” section of the chapter. Please take the time to read and study the details in the “Foundation Topics” section of the chapter, as well as review items noted with a Key Topic icon. 

Table  5-5 lists the protocols mentioned in this chapter and their respective standards documents. 

**Table 5-5** _Protocols and Standards for  Chapter  5_ 

|**Table 5-5** _Protocols and_|_Standards for  Chapter  5_|
|---|---|
|**Name**|**Standardized In**|
|ARP|RFC 826|
|Proxy ARP|RFC 1027|
|RARP|RFC 903|
|BOOTP|RFC 951|
|DHCP|RFC 2131|
|DHCP FQDN option|Internet-Draft|
|HSRP|Cisco proprietary|
|VRRP|RFC 3768|
|GLBP|Cisco proprietary|
|CDP|Cisco proprietary|
|NTP|RFC 1305|
|Syslog|RFC 5424|
|SNMP Version 1|RFCs 1155, 1156, 1157, 1212, 1213, 1215|
|SNMP Version 2|RFCs 1902–1907, 3416|
|SNMP Version 2c|RFC 1901|
|SNMP Version 3|RFCs 2578–2580, 3410–3415|
|Good Starting Point:|RFC 3410|



Table  5-6 lists some of the most popular Cisco IOS commands related to the topics in this chapter. 

260  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 5-6** _Command Reference for  Chapter  5_ 

|**Command**|**Description**|
|---|---|
|**ip dhcp pool ** _name_|Creates DHCP pool.|
|**default-router ** _address_|DHCP pool subcommand to list the gateways.|
|[_address2_..._address8_]||
|**dns-server ** _address_[_address2_..._address8_]|DHCP pool subcommand to list DNS servers.|
|**lease **{_days_[_hours_][_minutes_] |**infinite**}|DHCP pool subcommand to define the lease|
||length.|
|**network ** _network-number_[_mask_||DHCP pool subcommand to define IP addresses|
|_prefix-length_]|that can be assigned.|
|**ip dhcp excluded-address **[_low-address_|Global command to disallow these addresses|
|_high-address_]|from being assigned.|
|**host ** _address_[_mask_|_prefix-length_]|DHCP pool subcommand, used with_hardware-_|
||_address_or_client-identifier_, to predefine a|
||single host’s IP address.|
|**hardware-address ** _hardware-address_|DHCP pool subcommand to define MAC|
|_type_|address; works with the**host **command.|
|**show ip dhcp binding **[_ip-address_]|Lists addresses allocated by DHCP.|
|**show ip dhcp server statistics**|Lists stats for DHCP server operations.|
|**standby **[_group-number_]**ip **[_ip-address_|Interface subcommand to enable an HSRP group|
|[**secondary**]]|and define the virtual IP address.|
|**track ** _object-number_ **interface ** _type-_|Configures a tracking object that can be used by|
|_number_{_line-protocol_|_ip routing_}|HSRP, VRRP, or GLBP to track the status of an|
||interface.|
|**standby **[_group-number_]**preempt **[**delay**|Interface subcommand to enable preemption and|
|{**minimum ** _delay_|**reload ** _delay_|**sync**|set delay timers.|
|_delay_}]||
|**show track **[_object-number_[_brief_]|Displays status of tracked objects.|
||_interface_[_brief_] |**ip route **[_brief_]_|_||
|_resolution_|_timers_]||
|**standby **[_group-number_]**priority**|Interface subcommand to set the HSRP group|
|_priority_|priority for this router.|
|**standby **[_group-number_]**timers **[**msec**]|Interface subcommand to set HSRP group|
|_hellotime_[**msec**]_holdtime_|timers.|
|**standby **[_group-number_]**track ** _object-_|Interface subcommand to enable HSRP to track|
|_number_|defined objects, usually for the purpose of|
||switching active routers on an event related to|
||that object.|



Chapter 5: IP Services  261 

|**Command**|**Description**|
|---|---|
|**show standby **[_type number_[_group_]]|Lists HSRP statistics.|
|[**brief **|**all**]||
|**ntp peer ** _ip-address_[**version ** _number_]|Global command to enable symmetric active|
|[**key ** _keyid_] [**source ** _interface_] [**prefer**]|mode NTP.|
|**ntp server ** _ip-address_[**version ** _number_]|Global command to enable static client mode|
|[**key ** _keyid_] [**source ** _interface_] [**prefer**]|NTP.|
|**ntp broadcast **[**version ** _number_]|Interface subcommand on an NTP server to|
||cause NTP broadcasts on the interface.|
|**ntp broadcast client**|Interface subcommand on an NTP client to|
||cause it to listen for NTP broadcasts.|
|**ntp master **[_stratum_]|Global command to enable NTP server.|
|**show ntp associations**|Lists associations with other NTP servers and|
||clients.|
|**show ntp status**|Displays synchronization status, stratum level,|
||and other basic information.|
|**logging trap level**|Sets the severity level for syslog messages;|
||arguments are 0–7, where 0=emergencies,|
||1=alerts, 2=critical, 3=errors, 4=warnings,|
||5=notifications, 6=informational, 7=debugging|
||(default).|
|**logging host **{{_ip-address_|_hostname_}|Configures the IP or IPv6 address or host name|
|| {**ipv6 ** _ipv6-address_|_hostname_}}|to which to send syslog messages and permits|
|[**transport **{**udp **[**port ** _port-number_] |**tcp**|setting the transport protocol and port number.|
|[**port ** _port-number_]}] [**alarm **[_severity_]]||
|**ip wccp **{**web-cache **|_service-number_}|Enables WCCP and configures filtering and|
|[**service-list ** _service-access-list_]|service parameters.|
|[**mode **{**open **|**closed**}] [**group-address**||
|_multicast-address_] [**redirect-list ** _access-_||
|_list_] [**group-list ** _access-list_] [**password**||
|[**0-7**]_password_]||
|**ip wccp **{**web-cache **|_service-number_}|Interface configuration command to enable|
|**redirect **{**in **|**out**}|WCCP and configure it for outbound or|
||inbound service.|
|**show ip wccp**|Displays WCCP configuration settings and|
||statistics.|
|**snmp-server enable traps**|Enables sending of all types of traps available on|
||the router or switch.|



262  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

|**Command**|**Description**|
|---|---|
|**snmp-server host **{_hostname_||Configures the SNMP server to send traps or|
|_ip-address_} [**vrf ** _vrf-name_] [**traps **||informs to a particular host, along with options|
|**informs**] [**version **{**1 **|**2c **|**3 **[**auth **|**noauth**|for setting the SNMP version for traps and the|
||**priv**]}]**community-string **[**udp-port**|UDP port (default is 162). The notification-type|
|_port_] [_notification-type_]|field specifies the types of traps to send; if no|
||types are specified, all available categories of|
||traps will be sent.|
|**snmp-server community ** _string_[**view**|Sets the read-only or read-write community|
|_view-name_] [**ro **|**rw**] [_access-list-number_]|string and access list for host filtering for access|
||to SNMP reads and writes on the router or|
||switch.|
|**show snmp mib ifmib ifindex**|Shows the router’s interface ID for a particular|
|_interface-id_|interface. Particularly useful for RMON|
||configuration.|
|**ip sla monitor ** _operation-index_|Enters IP SLA monitor configuration mode for|
||an individual monitor function.|
|**type **[**jitter **|**udp-echo **|**echo protocol**|Configures the IP SLA monitor type with|
|**icmpecho **|**dns **|**ftp operation **|**http**|options (not shown) including source and|
|**operation **|**mpls ping ipv4 **|**pathecho **||destination IP address and source and|
|**pathjitter **|**tcpconnect **|**voip ** **delay**|destination port number, plus other relevant|
|**post-dial **|**udp-jitter **|**udp-jitter ** _codec_]|options to the particular type.|
|**ip sla key-chain ** _key-chain-name_|Configures a key chain for MD5 authentication|
||of IP SLA operations.|
|**ip sla monitor schedule ** _operation-_|Configures the schedule for a particular IP SLA|
|_number_[**life **{**forever **|_seconds_}] [**start-**|monitor. If the IP SLA monitor is deleted from|
|**time **{_hh_:_mm_[:_ss_] [_month day | day_|the configuration, the schedule is also deleted.|
|_month_] |**pending **|**now **|**after ** _hh_:_mm_:_ss_}]||
|[**ageout ** _seconds_] [**recurring**]||
|**ip sla monitor responder**|Enables the IP SLA responder function globally.|
||More specific options for this command can be|
||configured for specific responder types, ports,|
||and so on.|
|**show ip sla monitor statistics **[_operation_]|Shows the statistics for a specified IP SLA|
|**detail**|operation or all configured IP SLA operations.|
|**show ip sla responder**|Shows currently configured IP SLA responders|
||and recent activity (source IP address, and so|
||on).|
|**ip ssh **[**timeout ** _seconds_|**authentication-**|Sets SSH access crypto key.|
|**retries ** _integer_]||
|**crypto key generate rsa**|Generates RSA keys. Required for SSH|
||configuration.|



Chapter 5: IP Services  263 

|**Command**|**Description**|
|---|---|
|**transport input ssh**|In vty configuration mode, permits SSH|
||connections.|
|**ip http server**|Enables HTTP server.|
|**ip http secure-server**|Enables HTTPS server.|
|**ip traffic-export profile ** _profile-name_|Enables and enters configuration mode for a|
||RITE profile.|
|**ip traffic-export apply ** _profile-name_|Applies a RITE profile to an interface.|
|**event manager applet ** _applet-name_[**class**|Enters EEM applet configuration mode.|
|_class-options_] [**trap**]||
|**event cli pattern ** _regular-expression_|Configures EEM to match a CLI command|
|{[**default**] [**enter**] [**questionmark**] [**tab**]}|string.|
|[**sync **{**yes **|**no skip **{**yes **|**no**}] [**mode**||
|_variable_] [**occurs ** _num-occurrences_]||
|[**period ** _period-value_] [**maxrun**||
|_maxruntime-number_]||
|**ip flow-top-talkers**|NetFlow aggregator. Aggregates traffic for|
||unclassified top talkers.|
|**flow monitor ** _flow-name_|Enters configuration mode for a NetFlow|
||monitor.|
|**flow exporter ** _exporter-name_|Configures a NetFlow exporter and the|
||destination server to which to send NetFlow|
||information for a particular flow monitor.|
|**rmon event**|Configures an RMON event to monitor a|
||particular SNMP object, along with rising and|
||falling thresholds.|
|**rmon alarm**|Configures an alarm action for an RMON event’s|
||rising or falling threshold.|
|**Copy**|With FTP option in the source or destination|
||field, copies a file to or from an FTP server.|
|**tftp-server flash **[_partition-number:_]|Configures a TFTP server on the router to serve|
|_filename1_[**alias ** _filename2_] [_access-list-_|a file, optionally with an alias, and optionally|
|_number_]|through an ACL.|
|**aaa new-model**|Enables AAA on the router.|
|**aaa authentication**|Configures AAA authentication methods.|
|**aaa authorization**|Configures AAA authorization methods.|
|**ip scp server enable**|Enables the SCP server on the router. Requires|
||AAA authentication and AAA authorization to|
||be configured.|



264  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Memory Builders** 

The CCIE Routing and Switching written exam, like all Cisco CCIE written exams, covers a fairly broad set of topics. This section provides some basic tools to help you exercise your memory about some of the broader topics covered in this chapter.

## **Fill In Key Tables from Memory** 

Appendix  E , “Key Tables for CCIE Study,” on the CD in the back of this book, contains empty sets of some of the key summary tables in each chapter. Print  Appendix  E , refer to this chapter’s tables in it, and fill in the tables from memory. Refer to  Appendix  F , “Solutions for Key Tables for CCIE Study,” on the CD to check your answers.

## **Definitions** 

Next, take a few moments to write down the definitions for the following terms: 

HSRP, VRRP, GLBP, ARP, RARP, proxy ARP, BOOTP, DHCP, NTP symmetric active mode, NTP server mode, NTP client mode, NTP, virtual IP address, VRRP Master router, SNMP agent, SNMP manager, Get, GetNext, GetBulk, MIB-I, MIB-II, Response, Trap, Set, Inform, SMI, MIB, MIB walk, lead content engine 

Refer to the glossary to check your answers.

## **Further Reading** 

More information about several of the topics in this chapter can be easily found in a large number of books and online documentation. The RFCs listed in  Table  5-5 of the “Foundation Summary” section also provide a great deal of background information for this chapter. Here are a few references for more information about some of the less popular topics covered in this chapter: 

- **Proxy ARP:** www.cisco.com/en/US/tech/tk648/tk361/technologies_tech_note09186a0080094adb.shtml . 

- **GLBP:** www.cisco.com/en/US/docs/ios/12_2t/12_2t15/feature/guide/ft_glbp.html . 

- **VRRP:** www.cisco.com/en/US/docs/ios/12_0st/12_0st18/feature/guide/ st_vrrpx.html . 

- **SNMP:** Any further reading of SNMP-related RFCs should begin with RFC 3410, which provides a great overview of the releases and points to the more important of the vast number of SNMP-related RFCs. 

_This page intentionally left blank_ 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0307-00.png)

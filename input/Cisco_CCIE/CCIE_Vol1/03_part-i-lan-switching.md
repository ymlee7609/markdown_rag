## **Blueprint topics covered in this chapter:** 

This chapter covers the following subtopics from the Cisco CCIE Routing and Switching written exam blueprint. Refer to the full blueprint in Table I-1 in the Introduction for more details on the topics covered in each chapter and their context within the blueprint. 

- Ethernet 

- Speed 

- Duplex 

- Fast Ethernet 

- Gigabit Ethernet 

- SPAN, RSPAN, and ERSPAN 

- Virtual Switch System (VSS) 

- IOS-XE

## **CHAPTER 1**

## **Ethernet Basics** 

Ethernet has been the mainstay LAN protocol for years, and that is not anticipated to change anytime soon. More often than not, most people studying network and network fundamentals are very familiar with the protocol operations, its limitations, and its strengths. This level of familiarity often makes us complacent when it comes to determining a solid starting point for teaching technology. But when we consider how many technologies owe their capacity and capabilities to Ethernet, it becomes clear that this is the best place to start any discussion about networking. Ethernet is so established and useful that its role is expanding constantly. In fact, today it has even found its way into the WAN. Ethernet WAN technologies like Metro-Ethernet have changed the way we build geographically dispersed infrastructure and have paved the way for greater throughput in what was traditionally a slow and restrictive mode of transport. 

So with the understanding that the majority of readers are probably very familiar with Ethernet based on working with it on a day-to-day basis, we still need to ensure that we pay proper due diligence to the technology simply because it is so fundamental to the creation of both the most basic and the most complex network environments, and even though we are for the most part very knowledgeable about its operation, we might have forgotten some of the nuisances of its operation. So in this chapter, the intention is to outline those operations as clearly and succinctly as possible. 

For exam preparation, it is typically useful to use all the refresher tools: Take the “Do I Know This Already?” quiz, complete the definitions of the terms listed at the end of the chapter, print and complete the tables in  Appendix  E , “Key Tables for CCIE Study,” and certainly answer all the CD-ROM questions concerning Ethernet.

## **“Do I Know This Already?” Quiz** 

Table  1-1 outlines the major headings in this chapter and the corresponding “Do I Know This Already?” quiz questions. 

4  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 1-1** _“Do I Know This Already?” Foundation Topics Section-to-Question Mapping_ 

|**Table 1-1** _“Do I Know This Already?” Fou_|_ndation Topics Section-to-Questi_|_on Mappi_|
|---|---|---|
|**Foundation Topics Section**|**Questions Covered in This**|**Score**|
||**Section**||
|Ethernet Layer 1: Wiring, Speed, and Duplex|1–4||
|Ethernet Layer 2: Framing and Addressing|5–6||
|Switching and Bridging Logic|7||
|SPAN, RSPAN, and ERSPAN|8–9||
|Virtual Switch System|10–11||
|IOS Modernization|12||
|**Total Score**|||



To best use this pre-chapter assessment, remember to score yourself strictly. You can find the answers in  Appendix  A , “Answers to the ‘Do I Know This Already?’ Quizzes.” 

**1.** Which of the following denotes the correct usage of pins on the RJ-45 connectors at the opposite ends of an Ethernet crossover cable? 

   - **a.** 1 to 1 

   - **b.** 1 to 2 

   - **c.** 1 to 3 

   - **d.** 6 to 1 

   - **e.** 6 to 2 

   - **f.** 6 to 3 

**2.** Which of the following denotes the correct usage of pins on the RJ-45 connectors at the opposite ends of an Ethernet straight-through cable? 

   - **a.** 1 to 1 

   - **b.** 1 to 2 

   - **c.** 1 to 3 

   - **d.** 6 to 1 

   - **e.** 6 to 2 

   - **f.** 6 to 3 

Chapter 1: Ethernet Basics  5 

**3.** Which of the following commands must be configured on a Cisco IOS switch interface to disable Ethernet autonegotiation? 

   - **a. no auto-negotiate** 

   - **b. no auto** 

   - **c.** Both **speed** and **duplex** 

   - **d. duplex** 

   - **e. speed** 

**4.** Consider an Ethernet crossover cable between two 10/100 ports on Cisco switches. One switch has been configured for 100-Mbps full duplex. Which of the following is true about the other switch? 

   - **a.** It will use a speed of 10 Mbps. 

   - **b.** It will use a speed of 100 Mbps. 

   - **c.** It will use a duplex setting of half duplex. 

   - **d.** It will use a duplex setting of full duplex. 

**5.** Which of the following Ethernet header type fields is a 2-byte field? 

   - **a.** DSAP 

   - **b.** Type (in SNAP header) 

   - **c.** Type (in Ethernet V2 header) 

   - **d.** LLC Control 

**6.** Which of the following standards defines a Fast Ethernet standard? 

   - **a.** IEEE 802.1Q 

   - **b.** IEEE 802.3U 

   - **c.** IEEE 802.1X 

   - **d.** IEEE 802.3Z 

   - **e.** IEEE 802.3AB 

   - **f.** IEEE 802.1AD 

**7.** Suppose a brand-new Cisco IOS–based switch has just been taken out of the box and cabled to several devices. One of the devices sends a frame. For which of the following destinations would a switch flood the frames out all ports (except the port upon which the frame was received)? 

   - **a.** Broadcasts 

   - **b.** Unknown unicasts 

   - **c.** Known unicasts 

   - **d.** Multicasts 

- 6  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

   **8.** Which of the following configuration issues will keep a SPAN session from becoming active? 

      - **a.** Misconfigured destination port 

      - **b.** Destination port configured as a trunk 

      - **c.** Destination port shutdown 

      - **d.** Source port configured as a trunk 

   **9.** Which of the following are rules for SPAN configuration? 

      - **a.** SPAN source and destination ports must be configured for the same speed and duplex. 

      - **b.** If the SPAN source port is configured for 100 Mbps, the destination port must be configured for 100 Mbps or more. 

      - **c.** In a SPAN session, sources must consist of either physical interfaces or VLANs, but not a mix of these. 

      - **d.** Remote SPAN VLANs must be in the range of VLAN 1–66. 

      - **e.** Only three SPAN sessions can be configured on one switch. 

   **10.** What tool is available to reduce the complexity of a modern network infrastructure that has direct impact on both Layer 2 and Layer 3 design? 

      - **a.** Spanning Tree Protocol 

      - **b.** Bridge Assurance 

      - **c.** Virtual Switch Design 

      - **d.** Virtual Switching System 

      - **e.** IOS-XR 

   **11.** In a Virtual Switch System configuration, what operational component is used to transport Control, Management, and Data Plane traffic between peers? 

      - **a.** VPC-Link 

      - **b.** Sham-Link 

      - **c.** Virtual Switch Link 

      - **d.** Port-Channel 

      - **e.** Ether-Channel 

Chapter 1: Ethernet Basics  7 

**12.** Cisco IOS was expanded so that it could support modern enterprise deployments by moving away from a monolithic architecture to a more modular design model. What is this current version of IOS? 

   - **a.** CUOS 

   - **b.** IOS-NG 

   - **c.** LINUX 

   - **d.** IOS-XE 

   - **e.** IOS-version 2.0 

8  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Foundation Topics**

## **Ethernet Layer 1: Wiring, Speed, and Duplex** 

Before you make an Ethernet LAN functional, end-user devices, routers, and switches must be cabled correctly. To run with fewer transmission errors at higher speeds, and to support longer cable distances, variations of copper and optical cabling can be used. The different Ethernet specifications, cable types, and cable lengths per the various specifications are important for the exam, and are listed in the “Foundation Summary” section, later in this chapter.

## **RJ-45 Pinouts and Category 5 Wiring** 

You should know the details of crossover and straight-through Category 5 (Cat 5), Cat 5e, or Cat 6 cabling for almost any networking job. The EIA/TIA defines the cabling specifications for Ethernet LANs ( www.eia.org and  http://www.tiaonline.org ), including the pinouts for the RJ-45 connects, as shown in  Figure  1-1 . 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0049-06.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>



![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0049-07.png)


**Figure 1-1** _RJ-45 Pinouts with Four-Pair UTP Cabling_ 

The most popular Ethernet standards (10BASE-T and 100BASE-TX) each use two twisted pairs (specifically pairs 2 and 3 shown in  Figure  1-1 ), with one pair used for transmission in each direction. Depending on which pair a device uses to transmit and receive, either a straight-through or crossover cable is required.  Table  1-2 summarizes how the cabling and pinouts work. 

**Table 1-2** _Ethernet Cabling Types_ 

||**Table 1-2** _Ether_|_net Cabling Types_||
|---|---|---|---|
|**Key**||||
|**Topic**|**Type of Cable**|**Pinouts**|**Key Pins Connected**|
||Straight-through|T568A (both ends) or T568B (both ends)|1–1; 2–2; 3–3; 6–6|
||Crossover|T568A on one end, and T568B on the other|1–3; 2–6; 3–1; 6–2|



Chapter 1: Ethernet Basics  9 

Many Ethernet standards use two twisted pairs, with one pair being used for transmission in each direction. For example, a PC network interface card (NIC) transmits on pair 1,2 and receives on pair 3,6; switch ports do the opposite. So, a straight-through cable works well, connecting pair 1,2 on the PC (PC transmit pair) to the switch port’s pair 1,2, on which the switch receives. When the two devices on the ends of the cable both transmit using the same pins, a crossover cable is required. For example, if two connected switches send using the pair at pins 3,6 and receive on pins 1,2, the cable needs to connect the pair at 3,6 on one end to pins 1,2 at the other end, and vice versa. 

**Note** Crossover cables can also be used between a pair of PCs, swapping the transmit pair on one end (1,2) with the receive pins at the other end (3,6). 

Cisco also supports a switch feature that lets the switch figure out whether the wrong cable is installed: _Auto-MDIX_ (automatic medium-dependent interface crossover) detects the wrong cable and causes the switch to swap the pair it uses for transmitting and receiving, which solves the cabling problem. (As of publication, this feature is not supported on all Cisco switch models.)

## **Autonegotiation, Speed, and Duplex** 

By default, each Cisco switch port uses _Ethernet autonegotiation_ to determine the speed and duplex setting (half or full). The switches can also set their duplex setting with the **duplex interface** subcommand, and their speed with—you guessed it—the **speed interface** subcommand. 

Switches can dynamically detect the speed setting on a particular Ethernet segment by using a few different methods. Cisco switches (and many other devices) can sense the speed using the _Fast Link Pulses (FLP)_ of the autonegotiation process. However, if autonegotiation is disabled on either end of the cable, the switch detects the speed anyway based on the incoming electrical signal. You can force a speed mismatch by statically configuring different speeds on both ends of the cable, causing the link to no longer function. 

Switches detect duplex settings through autonegotiation only. If both ends have autonegotiation enabled, the duplex is negotiated. However, if either device on the cable disables autonegotiation, the devices without a configured duplex setting must assume a default. Cisco switches use a default duplex setting of half duplex (HDX) (for 10-Mbps and 100-Mbps interfaces) or full duplex (FDX) (for 1000-Mbps interfaces). To disable autonegotiation on a Cisco switch port, you simply need to statically configure the speed and the duplex settings. 

Ethernet devices can use FDX only when collisions cannot occur on the attached cable; a collision-free link can be guaranteed only when a shared hub is not in use. The next few topics review how Ethernet deals with collisions when they do occur, as well as what is different with Ethernet logic in cases where collisions cannot occur and FDX is allowed. 

10  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## CSMA/CD 

The original Ethernet specifications expected collisions to occur on the LAN. The media were shared, creating a literal electrical bus. Any electrical signal induced onto the wire could collide with a signal induced by another device. When two or more Ethernet frames overlap on the transmission medium at the same instant in time, a collision occurs; the collision results in bit errors and lost frames. 

The original Ethernet specifications defined the _Carrier Sense Multiple Access with Collision Detection (CSMA/CD)_ algorithm to deal with the inevitable collisions. CSMA/CD minimizes the number of collisions, but when they occur, CSMA/CD defines how the sending stations can recognize the collisions and retransmit the frame. The following list outlines the steps in the CSMA/CD process: 

**Key Topic** 

**1.** A device with a frame to send listens until the Ethernet is not busy (in other words, the device cannot sense a carrier signal on the Ethernet segment). 

**2.** When the Ethernet is not busy, the sender begins sending the frame. 

**3.** The sender listens to make sure that no collision occurred. 

**4.** If there was a collision, all stations that sent a frame send a jamming signal to ensure that all stations recognize the collision. 

**5.** After the jamming is complete, each sender of one of the original collided frames randomizes a timer and waits that long before resending. (Other stations that did not create the collision do not have to wait to send.) 

**6.** After all timers expire, the original senders can begin again with Step 1.

## Collision Domains and Switch Buffering 

A _collision domain_ is a set of devices that can send frames that collide with frames sent by another device in that same set of devices. Before the advent of LAN switches, Ethernets were either physically shared (10BASE2 and 10BASE5) or shared by virtue of shared hubs and their Layer 1 “repeat out all other ports” logic. Ethernet switches greatly reduce the number of possible collisions, both through frame buffering and through their more complete Layer 2 logic. 

By definition of the term, Ethernet hubs 

**Key Topic** 

- Operate solely at Ethernet Layer 1 

- Repeat (regenerate) electrical signals to improve cabling distances 

- Forward signals received on a port out all other ports (no buffering) 

As a result of a hub’s logic, a hub creates a single _collision domain_ . Switches, however, create a different collision domain per switch port, as shown in  Figure  1-2 . 

Chapter 1: Ethernet Basics  11 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0052-01.png)


**----- Start of picture text -----**<br>
1 Collision Domain Multiple Collision Domain<br>Key  10BASE-T, using Shared hub 10BASE-T, using Switch<br>Topic<br>Archie Archie<br>Hub1 SW1<br>Larry Larry<br>Bob Solid Lines Represent Bob<br>Twisted Pair Cabling<br>**----- End of picture text -----**<br>


**Figure 1-2** _Collision Domains with Hubs and Switches_ 

Switches have the same cabling and signal regeneration benefits as hubs, but switches do a lot more—including sometimes reducing or even eliminating collisions by buffering frames. When switches receive multiple frames on different switch ports, they store the frames in memory buffers to prevent collisions. 

For example, imagine that a switch receives three frames at the same time, entering three different ports, and they all must exit the same switch port. The switch simply stores two of the frames in memory, forwarding the frames sequentially. As a result, in  Figure  1-2 , the switch prevents any frame sent by Larry from colliding with a frame sent by Archie or Bob—which by definition puts each of the PCs attached to the switch in  Figure  1-2 in different collision domains. 

When a switch port connects through cable to a single other nonhub device—for example, like the three PCs in  Figure  1-2 —no collisions can possibly occur. The only devices that could create a collision are the switch port and the one connected device—and they each have a separate twisted pair on which to transmit. Because collisions cannot occur, such segments can use full-duplex logic. 

**Note** NICs operating in HDX mode use _loopback circuitry_ when transmitting a frame. This circuitry loops the transmitted frame back to the receive side of the NIC so that when the NIC receives a frame over the cable, the combined looped-back signal and received signal allows the NIC to notice that a collision has occurred.

## **Basic Switch Port Configuration** 

The three key configuration elements on a Cisco switch port are autonegotiation, speed, and duplex. Cisco switches use autonegotiation by default; it is then disabled if both the speed and duplex are manually configured. You can set the speed using the **speed** { **auto** | **10** | **100** | **1000** } interface subcommand, assuming that the interface supports multiple 

12  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

speeds. You configure the duplex setting using the **duplex** { **auto** | **half** | **full** } interface subcommand. 

Example  1-1 shows the manual configuration of the speed and duplex on the link between Switch1 and Switch4 from  Figure  1-3 , and the results of having mismatched duplex settings. (The book refers to specific switch commands used on IOS-based switches, referred to as “Catalyst IOS” by the Cisco CCIE blueprint.) 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0053-03.png)


**----- Start of picture text -----**<br>
0200.3333.3333 0/3<br>R3 SW1<br>0/13<br>000a.b7dc.b78d<br>000f.2343.87cd<br>0/13<br>0200.4444.4444 0/4<br>R4 SW4<br>0/6<br>0010.a49b.6111<br>PC1<br>**----- End of picture text -----**<br>


**Figure 1-3** _Simple Switched Network with Trunk_ 

**Example 1-1** _Manual Setting for Duplex and Speed, with Mismatched Duplex_ 

~~switch1#~~ **show interface fa 0/13** FastEthernet0/13 is up, line protocol is up Hardware is Fast Ethernet, address is 000a.b7dc.b78d (bia 000a.b7dc.b78d) MTU 1500 bytes, BW 100000 Kbit, DLY 100 usec, reliability 255/255, txload 1/255, rxload 1/255 Encapsulation ARPA, loopback not set Keepalive set (10 sec) ~~Full-duplex, 100Mb/s ! remaining lines omitted for brevity ! Below, Switch1's interface connecting to Switch4 is configured for 100 Mbps, ! HDX. Note that IOS rejects the first~~ ~~**duplex** command; you cannot set duplex until ! the speed is manually configured.~~ switch1# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. switch1(config)# **int fa 0/13** switch1(config-if)# **duplex half** ~~Duplex will not be set until speed is set to non-auto value~~ switch1(config-if)# **speed 100** 05:08:41: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/13, changed state þto down 

Chapter 1: Ethernet Basics  13 

05:08:46: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/13, changed state þto up switch1(config-if)# **duplex half** !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ~~! NOT SHOWN: Configuration for 100/half on Switch4's int fa 0/13.~~ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ~~! Now with both switches manually configured for speed and duplex, neither will be ! using Ethernet auto-negotiation. As a result, below the duplex setting on Switch1 ! can be changed to FDX with Switch4 remaining configured to use HDX.~~ switch1# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. switch1(config)# **int fa 0/13** switch1(config-if)# **duplex full** 05:13:03: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/13, changed state to down 05:13:08: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/13, changed state to up switch1(config-if)# **^Z** switch1# **sh int fa 0/13** FastEthernet0/13 is up, line protocol is up ~~! Lines omitted for brevity Full-duplex, 100Mb/s ! remaining lines omitted for brevity ! Below, Switch4 is shown to be HDX. Note ! the collisions counters at the end of the~~ ~~**show interface** command.~~ switch4# **sh int fa 0/13** FastEthernet0/13 is up, line protocol is up (connected) Hardware is Fast Ethernet, address is 000f.2343.87cd (bia 000f.2343.87cd) MTU 1500 bytes, BW 100000 Kbit, DLY 1000 usec, reliability 255/255, txload 1/255, rxload 1/255 Encapsulation ARPA, loopback not set Keepalive set (10 sec) ~~Half-duplex, 100Mb/s ! Lines omitted for brevity~~ 5 minute output rate 583000 bits/sec, 117 packets/sec 25654 packets input, 19935915 bytes, 0 no buffer Received 173 broadcasts (0 multicast) 0 runts, 0 giants, 0 throttles 0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored 0 watchdog, 173 multicast, 0 pause input 0 input packets with dribble condition detected 26151 packets output, 19608901 bytes, 0 underruns ~~54 output errors, 5 collisions, 0 interface resets 0 babbles, 54 late collision, 59 deferred~~ 0 lost carrier, 0 no carrier, 0 PAUSE output 0 output buffer failures, 0 output buffers swapped out 

14  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

~~02:40:49: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on FastEthernet0/13~~ 

**Key** ~~(not full duplex), with Switch1 FastEthernet0/13 (full duplex).~~ **Topic** 

~~! Above, CDP messages have been exchanged over the link between switches. CDP~~ 

~~! exchanges information about Duplex on the link, and can notice (but not fix) ! the mismatch.~~ 

The statistics on Switch4 near the end of the example show collisions (detected in the time during which the first 64 bytes were being transmitted) and late collisions (after the first 64 bytes were transmitted). In an Ethernet that follows cabling length restrictions, collisions should be detected while the first 64 bytes are being transmitted. In this case, Switch1 is using FDX logic, meaning that it sends frames anytime—including when Switch4 is sending frames. As a result, Switch4 receives frames anytime, and if sending at the time, it believes a collision has occurred. Switch4 has deferred 59 frames, meaning that it chose to wait before sending frames because it was currently receiving a frame. Also, the retransmission of the frames that Switch4 thought were destroyed because of a collision, but might not have been, causes duplicate frames to be received, occasionally causing application connections to fail and routers to lose neighbor relationships.

## **Ethernet Layer 2: Framing and Addressing** 

In this book, as in many Cisco courses and documents, the word _frame_ refers to the bits and bytes that include the Layer 2 header and trailer, along with the data encapsulated by that header and trailer. The term _packet_ is most often used to describe the Layer 3 header and data, without a Layer 2 header or trailer. Ethernet’s Layer 2 specifications relate to the creation, forwarding, reception, and interpretation of Ethernet frames. 

The original Ethernet specifications were owned by the combination of Digital Equipment Corp., Intel, and Xerox—hence the name “Ethernet (DIX).” Later, in the early 1980s, the IEEE standardized Ethernet, defining parts (Layer 1 and some of Layer 2) in the 802.3 _Media Access Control (MAC)_ standard, and other parts of Layer 2 in the 802.2 _Logical Link Control (LLC)_ standard. Later, the IEEE realized that the 1-byte Destination Service Access Point (DSAP) field in the 802.2 LLC header was too small. As a result, the IEEE introduced a new frame format with a _Sub-Network Access Protocol (SNAP)_ header after the 802.2 header, as shown in the third style of header in  Figure 1-4 . Finally, in 1997, the IEEE added the original DIX V2 framing to the 802.3 standard as well, as shown in the top frame in  Figure  1-4 . 

Table  1-3 lists the header fields, along with a brief explanation. The more important fields are explained in more detail after the table. 

Chapter 1: Ethernet Basics  15 

**Key Topic** 

**Key Topic** 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0056-03.png)


**----- Start of picture text -----**<br>
Ethernet (DIX) and Revised (1997) IEEE 802.3<br>8  6  6      2 Variable 4<br>Dest. Source Type/<br>Preamble Data FCS<br>Address Address Length<br>Original IEEE Ethernet (802.3)<br>7  1  6  6  2  1  1  1-2  Variable 4<br>D S<br>Dest. Source S S<br>Preamble SFD address address Length A A Control Data FCS<br>P P<br>802.3 802.2 802.3<br>IEEE 802.3 with SNAP Header<br>7  1  6  6  2  1  1  1-2  3           2     Variable    4<br>D S<br>Dest. Source S S<br>Preamble SFD address address Length A A Control OUI TYPE Data FCS<br>P P<br>802.3 802.2 SNAP 802.3<br>**----- End of picture text -----**<br>


**Figure 1-4** _Ethernet Framing Options_ 

**Table 1-3** _Ethernet Header Fields_ 

|**Field**|**Description**|
|---|---|
|Preamble (DIX)|Provides synchronization and signal transitions to allow proper|
||clocking of the transmitted signal. Consists of 62 alternating 1s|
||and 0s, and ends with a pair of 1s.|
|Preamble and Start of|Same purpose and binary value as DIX preamble; 802.3 simply|
|Frame Delimiter (802.3)|renames the 8-byte DIX preamble as a 7-byte preamble and a|
||1-byte Start of Frame Delimiter (SFD).|
|Type (or Protocol Type)|2-byte field that identifies the type of protocol or protocol|
|(DIX)|header that follows the header. Allows the receiver of the frame|
||to know how to process a received frame.|
|Length (802.3)|Describes the length, in bytes, of the data following the Length|
||field, up to the Ethernet trailer. Allows an Ethernet receiver to|
||predict the end of the received frame.|
|Destination Service|DSAP; 1-byte protocol type field. The size limitations, along|
|Access Point (802.2)|with other uses of the low-order bits, required the later addition|
||of SNAP headers.|
|Source Service Access|SSAP; 1-byte protocol type field that describes the upper-layer|
|Point (802.2)|protocol that created the frame.|
|Control (802.2)|1- or 2-byte field that provides mechanisms for both|
||connectionless and connection-oriented operation. Generally|
||used only for connectionless operation by modern protocols,|
||with a 1-byte value of 0x03.|



16  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

|**Field**|**Description**|
|---|---|
|Organizationally Unique|OUI; 3-byte field, generally unused today, providing a place|
|Identifier (SNAP)|for the sender of the frame to code the OUI representing the|
||manufacturer of the Ethernet NIC.|
|Type (SNAP)|2-byte Type field, using same values as the DIX Type field,|
||overcoming deficiencies with size and use of the DSAP field.|

## **Types of Ethernet Addresses** 

Ethernet addresses, also frequently called MAC addresses, are 6 bytes in length, typically listed in hexadecimal form. There are three main types of Ethernet address, as listed in Table  1-4 . 

**Table 1-4** _Three Types of Ethernet/MAC Address_ 

|||
|---|---|
|**Key**<br>**Topic**|**Type of Ethernet/**<br>**MAC Address**<br>**Description and Notes**|
||Unicast<br>Fancy term for an address that represents a single LAN interface. The<br>I/G bit, the least significant bit in the most significant byte, is set to 0.|
||Broadcast<br>An address that means “all devices that reside on this LAN right now.”<br>Always a value of hex FFFFFFFFFFFF.|
||Multicast<br>A MAC address that implies some subset of all devices currently on<br>the LAN. By definition, the I/G bit is set to 1.|



Most engineers instinctively know how unicast and broadcast addresses are used in a typical network. When an Ethernet NIC needs to send a frame, it puts its own unicast address in the Source Address field of the header. If it wants to send the frame to a particular device on the LAN, the sender puts the other device’s MAC address in the Ethernet header’s Destination Address field. If the sender wants to send the frame to every device on the LAN, it sends the frame to the FFFF.FFFF.FFFF broadcast destination address. (A frame sent to the broadcast address is named a _broadcast_ or _broadcast frame_ , and frames sent to unicast MAC addresses are called _unicasts_ or _unicast frames_ .) 

Multicast Ethernet frames are used to communicate with a possibly dynamic subset of the devices on a LAN. The most common use for Ethernet multicast addresses involves the use of IP multicast. For example, if only 3 of 100 users on a LAN want to watch the same video stream using an IP multicast–based video application, the application can send a single multicast frame. The three interested devices prepare by listening for frames sent to a particular multicast Ethernet address, processing frames destined for that address. Other devices might receive the frame, but they ignore its contents. Because the concept of Ethernet multicast is most often used today with IP multicast, most of the rest of the details of Ethernet multicast are covered in Volume 2,  Chapter  7 , “Introduction to IP Multicasting.” 

Chapter 1: Ethernet Basics  17 

**Key Topic**

## **Ethernet Address Formats** 

The IEEE intends for unicast addresses to be unique in the universe by administering the assignment of MAC addresses. The IEEE assigns each vendor a code to use as the first 3 bytes of its MAC addresses; that first half of the addresses is called the _Organizationally Unique Identifier (OUI)_ . The IEEE expects each manufacturer to use its OUI for the first 3 bytes of the MAC assigned to any Ethernet product created by that vendor. The vendor then assigns a unique value in the low-order 3 bytes for each Ethernet card that it manufactures—thereby ensuring global uniqueness of MAC addresses.  Figure 1-5 shows the basic Ethernet address format, along with some additional details. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0058-04.png)


**----- Start of picture text -----**<br>
Most Least<br>Significant Byte Significant Byte<br>1 [st]  Byte 2 [nd]  Byte 3 [rd]  Byte 4 [th]  Byte 5 [th]  Byte 6 [th]  Byte<br>OUI Vendor-Assigned<br>U/L I/G<br>Bit Bit<br>1 [st]  Byte<br>Most Least<br>Significant Significant<br>Bit Bit<br>**----- End of picture text -----**<br>


**Figure 1-5** _Ethernet Address Format_ 

Note that  Figure  1-5 shows the location of the most significant byte and least significant bit in each byte. IEEE documentation lists Ethernet addresses with the most significant byte on the left. However, inside each byte, the leftmost bit is the most significant bit, and the rightmost bit is the least significant bit. Many documents refer to the bit order as _canonical_ . Regardless of the term, the bit order inside each byte is important for understanding the meaning of the two most significant bits in an Ethernet address: 

- The Individual/Group (I/G) bit 

- The Universal/Local (U/L) bit 

Table  1-5 summarizes the meaning of each bit. 

18  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 1-5** _I/G and U/L Bits_ 

||**Table 1-5** _I/G and U/L Bits_|
|---|---|
|**Key**<br>**Topic**||
||**Field**<br>**Meaning**|
||I/G<br>Binary 0 means that the address is a unicast; Binary 1 means that the address is a<br>multicast or broadcast.|
||U/L<br>Binary 0 means that the address is vendor assigned; Binary 1 means that the<br>address has been administratively assigned, overriding the vendor-assigned<br>address.|



The I/G bit signifies whether the address represents an individual device or a group of devices, and the U/L bit identifies locally configured addresses. For example, the Ethernet multicast addresses used by IP multicast implementations always start with 0x01005E. Hex 01 (the first byte of the address) converts to binary 00000001, with the least significant bit being 1, confirming the use of the I/G bit. 

**Note** Often, when overriding the MAC address to use a local address, the device or device driver does not enforce the setting of the U/L bit to a value of 1.

## **Protocol Types and the 802.3 Length Field** 

Each of the three types of Ethernet header shown in  Figure  1-4 has a field identifying the format of the Data field in the frame. Generically called a _Type_ field, these fields allow the receiver of an Ethernet frame to know how to interpret the data in the received frame. For example, a router might want to know whether the frame contains an IP packet, an IPX packet, and so on. 

DIX and the revised IEEE framing use the Type field, also called the Protocol Type field. The originally defined IEEE framing uses those same 2 bytes as a Length field. To distinguish the style of Ethernet header, the Ethernet Type field values begin at 1536, and the length of the Data field in an IEEE frame is limited to decimal 1500 or less. That way, an Ethernet NIC can easily determine whether the frame follows the DIX or original IEEE format. 

The original IEEE frame used a 1-byte Protocol Type field (DSAP) for the 802.2 LLC standard type field. It also reserved the high-order 2 bits for other uses, similar to the I/G and U/L bits in MAC addresses. As a result, there were not enough possible combinations in the DSAP field for the needs of the market—so the IEEE had to define yet another type field, this one inside an additional IEEE SNAP header.  Table  1-6 summarizes the meaning of the three main Type field options with Ethernet. 

Chapter 1: Ethernet Basics  19 

**Key Topic** 

**Table 1-6** _Ethernet Type Fields_ 

|**Type Field**|**Description**|
|---|---|
|Protocol Type|DIX V2 Type field; 2 bytes; registered values now administered by the|
||IEEE|
|DSAP|802.2 LLC; 1 byte, with 2 high-order bits reserved for other purposes;|
||registered values now administered by the IEEE|
|SNAP|SNAP header; 2 bytes; uses same values as Ethernet Protocol Type;|
||signified by an 802.2 DSAP of 0xAA|

## **Switching and Bridging Logic** 

In this chapter so far, you have been reminded about the cabling details for Ethernet along with the formats and meanings of the fields inside Ethernet frames. A switch’s ultimate goal is to deliver those frames to the appropriate destination(s) based on the destination MAC address in the frame header.  Table  1-7 summarizes the logic used by switches when forwarding frames, which differs based on the type of destination Ethernet address and on whether the destination address has been added to its MAC address table. 

**Table 1-7** _LAN Switch Forwarding Behavior_ 

**Key Topic** 

|**Table 1-7** _LAN Sw_|_itch Forwarding Behavior_|
|---|---|
|**Type of Address**|**Switch Action**|
|Known unicast|Forwards frame out the single interface associated with the|
||destination address|
|Unknown unicast|Floods frame out all interfaces, except the interface on which the|
||frame was received|
|Broadcast|Floods frame identically to unknown unicasts|
|Multicast|Floods frame identically to unknown unicasts, unless multicast|
||optimizations are configured|



For unicast forwarding to work most efficiently, switches need to know about all the unicast MAC addresses and out which interface the switch should forward frames sent to each MAC address. Switches learn MAC addresses, and the port to associate with them, by reading the source MAC address of received frames. You can see the learning process in  Example  1-2 , along with several other details of switch operation.  Figure  1-6 lists the devices in the network associated with  Example  1-2 , along with their MAC addresses. 

20  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0061-01.png)


**----- Start of picture text -----**<br>
VLAN 1:<br>0200.3333.3333 0/3 IP Address       10.1.1.1<br>R3R3 SW1 MAC Address 000a.b7dc.b780<br>0/13<br>000a.b7dc.b78d<br>000f.2343.87cd<br>0/13<br>VLAN 1:<br>0200.4444.4444 0/4<br>IP Address       10.1.1.4<br>R4 SW4 MAC Address 000f.2343.87c0<br>0/6<br>0010.a49b.6111<br>PC1<br>**----- End of picture text -----**<br>


**Figure 1-6** _Sample Network with MAC Addresses Shown_ 

**Example 1-2** _Command Output Showing MAC Address Table Learning (Continued)_ 

Switch1# **show mac-address-table dynamic** Mac Address Table -----------------------------------------Vlan    Mac Address       Type       Ports ----    -----------       ----       ----- ~~1    000f.2343.87cd    DYNAMIC    Fa0/13~~ 1    0200.3333.3333    DYNAMIC    Fa0/3 1    0200.4444.4444    DYNAMIC    Fa0/13 Total Mac Addresses for this criterion: 3 ! Above, Switch1's MAC address table lists three dynamically learned addresses, ! including Switch4's FA 0/13 MAC. ! Below, Switch1 pings Switch4's management IP address. ~~Switch1#~~ **ping 10.1.1.4** 

Type escape sequence to abort. Sending 5, 100-byte ICMP Echos to 10.1.1.4, timeout is 2 seconds: !!!!! Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/4 ms 

~~! Below Switch1 now knows the MAC address associated with Switch4's management IP ! address. Each switch has a range of reserved MAC addresses, with the first MAC ! being used by the switch IP address, and the rest being assigned in sequence to ! the switch interfaces – note 0xcd (last byte of 2 nd address in the table above) ! is for Switch4's FA 0/13 interface, and is 13 (decimal) larger than Switch4's~~ 

~~! base MAC address.~~ 

Chapter 1: Ethernet Basics  21 

Switch1# **show mac-address-table dynamic** 

Mac Address Table 

------------------------------------------ 

Vlan    Mac Address       Type       Ports 

----    -----------       ----       ----- ~~1    000f.2343.87c0    DYNAMIC    Fa0/13~~ 

~~1    000f.2343.87cd    DYNAMIC    Fa0/13~~ 1    0200.3333.3333    DYNAMIC    Fa0/3 1    0200.4444.4444    DYNAMIC    Fa0/13 Total Mac Addresses for this criterion: 4 ~~! Not shown: PC1 ping 10.1.1.23 (R3) PC1's MAC in its MAC address table~~ ------------------------------------------ 

Vlan    Mac Address       Type       Ports ----    -----------       ----       ----1    000f.2343.87c0    DYNAMIC    Fa0/13 1    000f.2343.87cd    DYNAMIC    Fa0/13 1    0010.a49b.6111    DYNAMIC    Fa0/13 1    0200.3333.3333    DYNAMIC    Fa0/3 

~~1    0200.4444.4444    DYNAMIC    Fa0/13 Total Mac Addresses for this criterion: 5 ! Above, Switch1 learned the PC's MAC address, associated with FA 0/13, ! because the frames sent by the PC came into Switch1 over its FA 0/13. ! Below, Switch4's MAC address table shows PC1's MAC off its FA 0/6~~ switch4# **show mac-address-table dynamic** 

Mac Address Table 

------------------------------------------- 

Vlan    Mac Address       Type        Ports ----    -----------       --------    ----1    000a.b7dc.b780    DYNAMIC     Fa0/13 1    000a.b7dc.b78d    DYNAMIC     Fa0/13 1    0010.a49b.6111    DYNAMIC     Fa0/6 1    0200.3333.3333    DYNAMIC     Fa0/13 1    0200.4444.4444    DYNAMIC     Fa0/4 Total Mac Addresses for this criterion: 5 ~~! Below, for example, the aging timeout (default 300 seconds) is shown, followed ! by a command just listing the mac address table entry for a single address.~~ switch4# **show mac-address-table aging-time** Vlan    Aging Time ----    ---------- ~~1     300~~ switch4# **show mac-address-table address 0200.3333.3333** 

Mac Address Table 

22  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

------------------------------------------Vlan    Mac Address       Type        Ports ----    -----------       --------    ----- ~~1    0200.3333.3333    DYNAMIC     Fa0/13~~ Total Mac Addresses for this criterion: 1

## **SPAN, RSPAN, and ERSPAN** 

Cisco Catalyst switches support a method of directing all traffic from a source port or source VLAN to a single port. This feature, called SPAN (for Switch Port Analyzer) in the Cisco documentation and sometimes referred to as session monitoring because of the commands used to configure it, is useful for many applications. These include monitoring traffic for compliance reasons, for data collection purposes, or to support a particular application. For example, all traffic from a voice VLAN can be delivered to a single switch port to facilitate call recording in a VoIP network. Another common use of this feature is to support intrusion detection/prevention system (IDS/IPS) security solutions. 

SPAN sessions can be sourced from a port or ports, or from a VLAN. This provides great flexibility in collecting or monitoring traffic from a particular source device or an entire VLAN. 

The destination port for a SPAN session can be on the local switch, as in SPAN operation. Or it can be a port on another switch in the network. This mode is known as Remote SPAN, or RSPAN. In RSPAN, a specific VLAN must be configured across the entire switching path from the source port or VLAN to the RSPAN destination port. This requires that the RSPAN VLAN be included in any trunks in that path, too. See  Figure 1-7 for the topology of SPAN,  Figure  1-8 for that of RSPAN, and  Figure  1-9 for that of Encapsulated Remote SPAN (ERSPAN). 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0063-06.png)



![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0063-07.png)



![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0063-08.png)


**----- Start of picture text -----**<br>
Egress<br>Traffic<br>Sniffer<br>Switch<br>Ingress<br>Traffic<br>Source Span Destination Span<br>Ports Port<br>**----- End of picture text -----**<br>


**Figure 1-7** _SPAN Topology_ 

Chapter 1: Ethernet Basics  23 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0064-01.png)


**----- Start of picture text -----**<br>
Switch S1 Switch S2<br>ISL TRUNK<br>6/1 5/1 5/2 Sniffer<br>A<br>**----- End of picture text -----**<br>


**Figure 1-8** _RSPAN Topology_ 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0064-03.png)


**----- Start of picture text -----**<br>
Host B<br>GRE-Encapsulated<br>SPAN<br>Monitored Traffic<br>Source<br>Device Device<br>Host A<br>IP/MPLS Cloud<br>SPAN<br>Destination<br>Network Analyzer<br>**----- End of picture text -----**<br>


**Figure 1-9** _ERSPAN Topology_ 

The information in this section applies specifically to the Cisco 3560 switching platform; the Cisco 3750 and many other platforms use identical or similar rules and configuration commands.

## **Core Concepts of SPAN, RSPAN, and ERSPAN** 

To understand SPAN, RSPAN, and ERSPAN, it helps to break them down into their fundamental elements. This also helps you understand how to configure these features. 

In SPAN, you create a SPAN source that consists of at least one port or at least one VLAN on a switch. On the same switch, you configure a destination port. The SPAN source data is then gathered and delivered to the SPAN destination. 

In RSPAN, you create the same source type—at least one port or at least one VLAN. The destination for this session is the RSPAN VLAN, rather than a single port on the switch. At the switch that contains an RSPAN destination port, the RSPAN VLAN data is delivered to the RSPAN port. 

24  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

In ERSPAN, we are actually encapsulating the Remote SPAN information. Encapsulated Remote SPAN (ERSPAN), as the name implies, creates a generic routing encapsulation (GRE) tunnel for all captured traffic and allows it to be extended across Layer 3 domains. This feature is an operational enhancement brought to us by IOS-XE and can be found in current platforms like the ASR 1000, but keep in mind that ERSPAN is also supported by the Catalyst 6500, 7600, as well as the Nexus platforms. Viable monitoring sources include Fast Ethernet, Gigabit Ethernet, and Port-Channel interfaces. 

**Key Topic** 

Regardless of the type of SPAN we are running, a SPAN source port can be any type of port—a routed port, a physical switch port, an access port, a trunk port, an EtherChannel port (either one physical port or the entire port-channel interface), and so on. On a SPAN source VLAN, all active ports in that VLAN are monitored. As you add or remove ports from that VLAN, the sources are dynamically updated to include new ports or exclude removed ports. Also, a port configured as a SPAN destination cannot be part of a SPAN source VLAN.

## **Restrictions and Conditions** 

Destination ports in SPAN, RSPAN, and ERSPAN have multiple restrictions. The key restrictions include the following: 

- When you configure a destination port, its original configuration is overwritten. If the SPAN configuration is removed, the original configuration on that port is restored. 

- When you configure a destination port, the port is removed from any EtherChannel bundle if it were part of one. If it were a routed port, the SPAN destination configuration overrides the routed port configuration. 

- Destination ports do not support port security, 802.1x authentication, or private VLANs. In general, SPAN/RSPAN and 802.1x are incompatible. 

- Destination ports do not support any Layer 2 protocols, including CDP, Spanning Tree, VTP, DTP, and so on. 

A set of similar restrictions for RSPAN destination VLANs also exists. See the references in the “Further Reading” section at the end of this chapter for more information about those restrictions. 

**Key Topic** 

SPAN, RSPAN, and ERSPAN require compliance with a number of specific conditions to work. For SPAN, the key restrictions include the following: 

- The source can be either one or more ports or a VLAN, but not a mix of these. 

- Up to 64 SPAN destination ports can be configured on a switch. 

- Switched or routed ports can be configured as SPAN source ports or SPAN destination ports. 

Chapter 1: Ethernet Basics  25 

- Be careful to avoid overloading the SPAN destination port. A 100-Mbps source port can easily overload a 10-Mbps destination port; it’s even easier to overload a 100Mbps destination port when the source is a VLAN. 

- Within a single SPAN session, you cannot deliver traffic to a destination port when it is sourced by a mix of SPAN, RSPAN, or ERSPAN source ports or VLANs. This restriction comes into play when you want to mirror traffic to both a local port on a switch (in SPAN) and a remote port on another switch (in RSPAN or ERSPAN mode). 

- A SPAN destination port cannot be a source port, and a source port cannot be a destination port. 

- Only one SPAN/RSPAN/ERSPAN session can send traffic to a single destination port. 

- A SPAN destination port ceases to act as a normal switch port. That is, it passes only SPAN-related traffic. 

- It’s possible to configure a trunk port as the source of a SPAN or RSPAN session. In this case, all VLANs on the trunk are monitored by default; the **filter vlan** command option can be configured to limit the VLANs being monitored in this situation. 

- Traffic that is routed from another VLAN to a source VLAN cannot be monitored with SPAN. An easy way to understand this concept is that only traffic that enters or exits the switch in a source port or VLAN is forwarded in a SPAN session. In other words, if the traffic comes from another source within the switch (by routing from another VLAN, for example), that traffic isn’t forwarded through SPAN. 

SPAN, RSPAN, and ERSPAN support three types of traffic: transmitted, received, and both. By default, SPAN is enabled for traffic both entering and exiting the source port or VLAN. However, SPAN can be configured to monitor just transmitted traffic or just received traffic. Some additional conditions apply to these traffic types, as detailed in this list: 

**Key Topic** 

- For Receive (RX) SPAN, the goal is to deliver all traffic received to the SPAN destination. As a result, each frame to be transported across a SPAN connection is copied and sent before any modification (for example, VACL or ACL filtering, QoS modification, or even ingress or egress policing). 

- For Transmit (TX) SPAN, all relevant filtering or modification by ACLs, VACLs, QoS, or policing actions are taken before the switch forwards the traffic to the SPAN/ RSPAN destination. As a result, not all transmit traffic necessarily makes it to a SPAN destination. Also, the frames that are delivered do not necessarily match the original frames exactly, depending on policies applied before they are forwarded to the SPAN destination. 

- A special case applies to certain types of Layer 2 frames. SPAN/RSPAN usually ignores CDP, spanning-tree BPDUs, VTP, DTP, and PAgP frames. However, these traffic types can be forwarded along with the normal SPAN traffic if the **encapsulation replicate** command is configured. 

26  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Basic SPAN Configuration** 

The goal for the configuration in  Example  1-3 is to mirror traffic sent to or received from interface fa0/12 to interface fa0/24. All traffic sent or received on fa0/12 is sent to fa0/24. This configuration is typical of a basic traffic-monitoring application. 

**Example 1-3** _Basic SPAN Configuration Example_ 

MDF-ROC1# **configure terminal** MDF-ROC1(config)# **monitor session 1 source interface fa0/12** MDF-ROC1(config)# **monitor session 1 destination interface fa0/24**

## **Complex SPAN Configuration** 

In  Example  1-4 , we configure a switch to send the following traffic to interface fa0/24, preserving the encapsulation from the sources: 

- Received on interface fa0/18 

- Sent on interface fa0/9 

- Sent and received on interface fa0/19 (which is a trunk) 

We also filter (remove) VLANs 1, 2, 3, and 229 from the traffic coming from the fa0/19 trunk port. 

**Example 1-4** _Complex SPAN Configuration Example_ 

MDF-ROC3# **config term** MDF-ROC3(config)# **monitor session 11 source interface fa0/18 rx** MDF-ROC3(config)# **monitor session 11 source interface fa0/9 tx** MDF-ROC3(config)# **monitor session 11 source interface fa0/19** MDF-ROC3(config)# **monitor session 11 filter vlan 1 - 3 , 229** MDF-ROC3(config)# **monitor session 11 destination interface fa0/24 encapsulation replicate**

## **RSPAN Configuration** 

In  Example  1-5 , we configure two switches, IDF-SYR1 and IDF-SYR2, to send traffic to RSPAN VLAN 199, which is delivered to port fa0/24 on switch MDF-SYR9 as follows: 

- From IDF-SYR1, all traffic received on VLANs 66–68 

- From IDF-SYR2, all traffic received on VLAN 9 

- From IDF-SYR2, all traffic sent and received on VLAN 11 

Note that all three switches use a different session ID, which is permissible in RSPAN. The only limitation on session numbering is that the session number must be 1 to 66. 

Chapter 1: Ethernet Basics  27 

**Example 1-5** _RSPAN Configuration Example_ 

IDF-SYR1# **config term** IDF-SYR1(config)# **vlan 199** IDF-SYR1(config-vlan)# **remote span** IDF-SYR1(config-vlan)# **exit** IDF-SYR1(config)# **monitor session 3 source vlan 66 – 68 rx** IDF-SYR1(config)# **monitor session 3 destination remote vlan 199** !Now moving to IDF-SYR2: IDF-SYR2# **config term** IDF-SYR2(config)# **vlan 199** IDF-SYR2(config-vlan)# **remote span** IDF-SYR2(config-vlan)# **exit** IDF-SYR2(config)# **monitor session 23 source vlan 9 rx** IDF-SYR2(config)# **monitor session 23 source vlan 11** IDF-SYR2(config)# **monitor session 23 destination remote vlan 199** !Now moving to MDF-SYR9 MDF-SYR9# **config term** MDF-SYR9(config)# **vlan 199** MDF-SYR9(config-vlan)# **remote span** MDF-SYR9(config-vlan)# **exit** MDF-SYR9(config)# **monitor session 63 source remote vlan 199** MDF-SYR9(config)# **monitor session 63 destination interface fa0/24** MDF-SYR9(config)# **end**

## **ERSPAN Configuration** 

In  Example  1-6 , we will configure ASR 1002 to capture received traffic and send to it to Catalyst 6509 Gig2/2/1. This traffic will simply be captured, encapsulated in GRE by ASR 1002 natively, and routed over to the Catalyst 6509. A sniffing station on the 6500 attached to GE2/2/1 will see the complete Ethernet frame (L2 to L7) information. 

**Example 1-6** _ERSPAN Configuration Example_ 

ASR1002(config)# **monitor session 1 type erspan-source** ASR1002(config-mon-erspan-src)# **source interface gig0/1/0 rx** ASR1002(config-mon-erspan-src)# **no shutdown** ASR1002(config-mon-erspan-src)# **destination** ASR1002(config-mon-erspan-src-dst)# **erspan-id 101** ASR1002(config-mon-erspan-src-dst)# **ip address 10.1.1.1** ASR1002(config-mon-erspan-src-dst)# **origin ip address 172.16.1.1** !Now for the configuration of the Catalyst 6500 SW6509(config)# **monitor session 2 type erspan-destination** SW6509(config-mon-erspan-dst)# **destination interface gigabitEthernet2/2/1** SW6509(config-mon-erspan-dst)# **no shutdown** SW6509(config-mon-erspan-dst)# **source** SW6509(config-mon-erspan-dst-src)# **erspan-id 101** SW6509(config-mon-erspan-dst-src)# **ip address 10.1.1.1** 

28  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

You can verify SPAN, RSPAN, or ERSPAN operation using the **show monitor session Key** command, as illustrated in  Example  1-7 . **Topic** 

**Example 1-7** _ERSPAN Verification Example_ 

ASR1002# **show monitor session 1** Session 1 --------Type                   : ERSPAN Source Session Status                 : Admin Enabled Source Ports           : RX Only           : Gi0/1/0 Destination IP Address : 10.1.1.1 MTU                   : 1464 Destination ERSPAN ID : 101 Origin IP Address    : 172.16.1.1 

From a troubleshooting standpoint, it’s important to note that if the destination port is shut down, the SPAN instance won’t come up. When you bring the port up, the SPAN session will follow.

## **Virtual Switch System** 

In any modern network, we find it essential to create topologies that support high availability and reliability of devices, connections, and services. The typical approach employed by network operators is to configure these features and capabilities by creating redundant Layer 2 switch fabric such that it will support multipathing through the use of redundant pairs or links.  Figure  1-10 shows a typical switch network configuration. 

Observe that the application and configuration of these redundant network elements and links we are describing can very quickly increase the complexity of our network design and operation. One method of overcoming this complication is to employ virtual switching. This technology actually simplifies the network by reducing the number of network elements, and this eliminates or masks the complexity of managing redundant switches and links. This feature exists in Cisco Catalyst 6500 and 4500 Series switches running IOS-XE (discussed in further detail in the section, “IOS-XE,” later in this chapter). 

For the purposes of our discussions, we will look at a Virtual Switch System (VSS) that combines a pair of Catalyst 4500 or 4500-X Series switches into a single network element. The VSS manages the redundant links in such a fashion that they will be seen by external devices as a single Port-channel. 

This approach simplifies network configuration and operation by reducing the total number of Layer 3 routing neighbors and by simultaneously providing a loop-free Layer 2 topology. 

Chapter 1: Ethernet Basics  29 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0070-01.png)


**----- Start of picture text -----**<br>
Core<br>Distribution<br>Access<br>**----- End of picture text -----**<br>


**Figure 1-10** _Typical Switch Network Design_

## **Virtual Switching System** 

The fundamental reason for employing a VSS is to logically combine a pair of switches into a single network element, as already described. To better understand this process, we need to look closely at what this feature does for the logical topology. For example, a VSS in the distribution layer of the network interacts with the access and core networks above and below it as if it were a single switch, as illustrated in  Figure  1-11 . 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0070-05.png)


**----- Start of picture text -----**<br>
Physical View Logical View<br>Virtual Distribution Switch Virtual Distribution Switch<br>Access Access<br>**----- End of picture text -----**<br>


**Figure 1-11** _VSS in the Distribution Network_ 

Notice that a switch in the access layer connects to both switches of the VSS using one logical port channel because the VSS is perceived as being a single switch to external devices—a logical switch if you will. Special adaptations are incorporated into the VSS 

30  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

devices such that they can manage redundancy and load balancing on the port channel to ensure managed operation of the link, even though it is physically connected to two devices. The inclination here would be to describe these switches inside the VSS configuration as independent devices; however, this is not accurate. Though the switches are physically separate entities, it must be understood that from an operation and control plane level, they are acting as one unit. This adaptation enables a loop-free Layer 2 network topology. The VSS also simplifies the Layer 3 network topology by reducing the number of routing peers in the network, thus extending network simplification into the data plane itself.

## **VSS Active and VSS Standby Switch** 

The adoption that we have been discussing regarding the operation of each device in a VSS extends to specialized “role based” behaviors. Now in the context of the VSS, we will find that each individual switch will first contend for specific operational roles inside the VSS process itself and then behave according to those roles. Each time that we create or restart a VSS, the peer switches will negotiate their roles. The ultimate outcome will be that one device will become the VSS active switch, and the other will become the VSS standby. 

The VSS active switch controls the VSS, running the Layer 2 and Layer 3 control protocols for the switching modules on both switches. The VSS active switch also provides management functions for the VSS, such as module online insertion and removal (OIR) and the console interface. 

The VSS active and standby switches perform packet forwarding for ingress data traffic on their locally hosted interfaces. However, the VSS standby switch sends all control traffic to the VSS active switch for processing.

## **Virtual Switch Link** 

As mentioned previously, for the two switches of the VSS to act as one network element, they need to share control information and data traffic, and the manner in which they perform this sharing extends to the roles that they have assumed and many specialpurpose mechanisms. Of these special-purpose constructs, none are more important that the virtual switch link that connects the two VSS devices. 

The virtual switch link (VSL) is a special link that carries control and data traffic between the two switches of a VSS, as shown in  Figure  1-12 . The VSL is typically implemented as an EtherChannel, and as such, can support up to eight links incorporated into the bundle. Not only is this special-purpose link designed to provide an avenue of communication between the VSS peers, but it is also optimized to provide control and management plane traffic higher priority than data traffic in an effort to ensure that control and management messages are never discarded. Data traffic is load balanced among the VSL links by either the default or the configured EtherChannel load-balancing algorithm. 

Chapter 1: Ethernet Basics  31 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0072-01.png)


**----- Start of picture text -----**<br>
Virtual Switch<br>Chassis 1 Chassis 2<br>Virtual Switch Link<br>(VSL)<br>**----- End of picture text -----**<br>


**Figure 1-12** _Virtual Switch Link_

## **Multichassis EtherChannel (MEC)** 

Note that we have been speaking significantly about the idea of EtherChannel. EtherChannel (also known as a port channel) is a collection of two or more physical links that combine to form one logical link. Layer 2 protocols operate on the EtherChannel as a single logical entity. This extends to protocols like Spanning Tree Protocol, which would normally serve to block redundant links between devices in an effort to prevent the formation of switching loops. But the notion that we are describing is a special kind of Port-channel that can exist not between two physical devices, but between multiple chassis. This affords us a hardware or device failover capability that does not exist in normal EtherChannel deployments. This is because VSS enables the creation of Multichassis EtherChannel (MEC), which is an EtherChannel whose member ports can be distributed across the member switches in a VSS. Because non-VSS switches connected to a VSS view the MEC as a standard EtherChannel, non-VSS switches can connect in a dual-homed manner. Traffic traversing the MEC can be load balanced locally within a VSS member switch much like that of standard EtherChannels. Cisco MEC supports dynamic EtherChannel protocols, to include the industry-standard Link Aggregation Control Protocol (LACP) and the Cisco-proprietary Port Aggregation Protocol (PAgP), as well as static EtherChannel configuration. In total, a VSS can support a maximum of 256 EtherChannels. This limit applies to the total number of regular EtherChannels and MECs.

## **Basic VSS Configuration** 

To create the most basic configuration needed to support VSS, first you have to create the same virtual switch domain on both sides of the VSS. This switch domain will be referenced as a number used on both switches of the VSS; this number must fall between 1 and 255. After assigning the domain number, you must configure one switch to be switch number 1 and the other switch to be switch number 2, as illustrated in  Example  1-8 . 

32  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Example 1-8** _Assigning Virtual Switch Domain and Switch Numbers_ 

SW1# **conf t** Enter configuration commands, one per line. End with CNTL/Z. SW1(config)# **switch virtual domain 10** Domain ID 10 config will take effect only after the exec command 'switch convert mode virtual' is issued SW1(config-vs-domain)# **switch 1** SW1(config-vs-domain)# **exit** SW1(config)# SW2# **conf t** Enter configuration commands, one per line. End with CNTL/Z. SW2(config)# **switch virtual domain 10** Domain ID 10 config will take effect only after the exec command 'switch convert mode virtual' is issued SW2(config-vs-domain)# **switch 2** SW2(config-vs-domain)# **exit** SW2(config)# 

Next, we will need to create the VSL, which requires a unique port channel on each switch, as shown in  Example  1-9 . During the configuration, both port channels are set up on the VSS active switch. If the VSS standby switch VSL port channel number has been configured previously for another use, the VSS will come up in route processor redundancy mode. To avoid this situation, check that both port channel numbers are available on both of the peer switches. 

**Example 1-9** _Configuring VSL Port Channel_ 

SW1(config)# **int port-channel 5** SW1(config-if)# **switchport** SW1(config-if)# **switch virtual link 1** SW1(config-if)# **no shut** SW1(config-if)# **exit** *Jan 24 05:19:57.092: %SPANTREE-6-PORTDEL_ALL_VLANS: Port-channel5 deleted from all Vlans SW2(config)# **int port-channel 10** SW2(config-if)# **switchport** SW2(config-if)# **switch virtual link 2** SW2(config-if)# **no shut** SW2(config-if)# **exit** SW2(config)# *Jan 24 05:14:17.273: %SPANTREE-6-PORTDEL_ALL_VLANS: Port-channel10 deleted from all Vlans 

Chapter 1: Ethernet Basics  33 

Now that we have created the Port-channel interfaces, it is necessary to add VSL physical member ports to the appropriate Port-channel. In  Example  1-10 , interfaces Gigabit Ethernet 7/3 and 7/4 on Switch 1 are going to be connected to interfaces Gigabit Ethernet 4/45 and 4/46 on Switch 2. 

**Example 1-10** _Configuring VSL Ports_ 

SW1(config)# **int range gig7/3 - 4** SW1(config-if-range)# **switchport mode trunk** SW1(config-if-range)# **channel-group 5 mode on** WARNING: Interface GigabitEthernet7/3 placed in restricted config mode. All extraneous configs removed! WARNING: Interface GigabitEthernet7/4 placed in restricted config mode. All extraneous configs removed! SW1(config-if-range)# **exit** SW2(config)# **int range gig4/45 - 46** SW2(config-if-range)# **switchport mode trunk** SW2(config-if-range)# **channel-group 10 mode on** WARNING: Interface GigabitEthernet4/45 placed in restricted config mode. All extraneous configs removed! WARNING: Interface GigabitEthernet4/46 placed in restricted config mode. All extraneous configs removed! SW2(config-if-range)# **exit** 

**Note** After the interfaces are put into a VSL Port-channel with the **channel-group** command, the interfaces go into “notconnect” status. Interface status will show “up,” but the line protocol will be “down.” The interface will be in up/down (not connect) status until the switch is rebooted. 

Now we will need to complete the switch conversion process by implementing the **switch convert mode virtual** command on Switch 1. The system will prompt to confirm the action. Enter yes, as illustrated in  Example  1-11 . This will allow the system to create a converted configuration file that will be stored in the system bootflash. 

**Example 1-11** _Converting the Switch to Virtual Switch Mode_ 

SW1# **switch convert mode virtual** This command will convert all interface names to naming convention "interface-type switch-number/slot/port", save the running config to startup-config and reload the switch. ~~Do you want to proceed? [yes/no]:~~ ~~**yes**~~ Converting interface names 

34  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Building configuration... Compressed configuration from 6551 bytes to 2893 bytes[OK] Saving converted configuration to bootflash: ... Destination filename [startup-config.converted_vs-20130124-062921]? Please stand by while rebooting the system... Restarting system. Rommon (G) Signature verification PASSED Rommon (P) Signature verification PASSED FPGA   (P) Signature verification PASSED Similarly you need to enter the "switch convert mode virtual" command on Switch 2 for converting to Virtual Switch Mode. 

SW2# **switch convert mode virtual** 

This command will convert all interface names to naming convention "interface-type switch-number/slot/port", save the running config to startup-config and reload the switch. ~~Do you want to proceed? [yes/no]:~~ ~~**yes**~~ Converting interface names Building configuration... Compressed configuration from 6027 bytes to 2774 bytes[OK] Saving converted configuration to bootflash: ... Destination filename [startup-config.converted_vs-20130124-052526]? Please stand by while rebooting the system... Restarting system. 

Rommon (G) Signature verification PASSED Rommon (P) Signature verification PASSED FPGA   (P) Signature verification PASSED 

************************************************************ *                                                          * * Welcome to Rom Monitor for   WS-X45-SUP7-E System.       * * Copyright (c) 2008-2012 by Cisco Systems, Inc.           * * All rights reserved.                                     * *                                                          * ************************************************************ 

After confirmation is completed on each switch, the running configuration will be saved as the startup configuration and the switch will reboot. After the reboot, the switch will be in virtual switch mode. 

Chapter 1: Ethernet Basics  35

## **VSS Verification Procedures** 

A handful of simple **show** commands can be used to display specifics associated with the VSS configuration of a particular VSS pair. The virtual switch domain number, and the switch number and role for each of the switches, can be found through the **show switch virtual** command, as illustrated in  Example  1-12 . 

**Example 1-12** _Display the Virtual Switch Domain Number_ 

SW1# **sh switch virtual** Executing the command on VSS member switch role = VSS Active, id = 1 Switch mode                  : Virtual Switch Virtual switch domain number : 10 Local switch number          : 1 Local switch operational role: Virtual Switch Active Peer switch number           : 2 Peer switch operational role : Virtual Switch Standby Executing the command on VSS member switch role = VSS Standby, id = 2 Switch mode                  : Virtual Switch Virtual switch domain number : 10 Local switch number          : 2 Local switch operational role: Virtual Switch Standby Peer switch number           : 1 Peer switch operational role : Virtual Switch Active 

One of the most important operational requirements of a VSS is to ensure that one switch in the cluster is the active switch and the other is the standby. The console of the standby switch should appear as illustrated in  Example  1-13 . 

**Example 1-13** _Console of the Standby Switch_ 

SW2-standby> Standby console disabled 

As we described in the theoretical portion of our discussion, there are a number of roles and configurational requirements associated with VSS. To see these variables for each of the switches in the VSS, use the **show switch virtual role** command.  Example  1-14 shows the type and detail that this command can generate. 

36  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Example 1-14** _Virtual Role Assignment and Priority_ 

SW1# **sh switch virtual role** Executing the command on VSS member switch role = VSS Active, id = 1 RRP information for Instance 1 -------------------------------------------------------------------Valid Flags   Peer     Preferred Reserved Count     Peer       Peer -------------------------------------------------------------------TRUE   V       1           1         1 Switch Switch Status Preempt       Priority Role     Local   Remote Number         Oper(Conf)   Oper(Conf)         SID     SID -------------------------------------------------------------------LOCAL   1     UP     FALSE(N )     100(100) ACTIVE   0       0 REMOTE  2     UP     FALSE(N )     100(100) STANDBY 6834   6152 Peer 0 represents the local switch Flags : V - Valid In dual-active recovery mode: No Executing the command on VSS member switch role = VSS Standby, id = 2 RRP information for Instance 2 -------------------------------------------------------------------Valid Flags   Peer     Preferred Reserved Count     Peer       Peer -------------------------------------------------------------------TRUE    V       1           1         1 Switch Switch Status Preempt       Priority Role     Local   Remote Number         Oper(Conf)   Oper(Conf)         SID     SID -------------------------------------------------------------------LOCAL   2     UP     FALSE(N )     100(100) STANDBY  0       0 REMOTE  1     UP     FALSE(N )     100(100) ACTIVE   6152   6834 Peer 0 represents the local switch Flags : V - Valid In dual-active recovery mode: No 

To display information about the VSL, use the **show switch virtual link** command, as shown in  Example  1-15 . 

Chapter 1: Ethernet Basics  37 

**Example 1-15** _Virtual Switch Link Details_ 

SW1# **sh switch virtual link** Executing the command on VSS member switch role = VSS Active, id = 1 VSL Status : UP VSL Uptime : 3 minutes VSL Control Link : Gi1/7/4 Executing the command on VSS member switch role = VSS Standby, id = 2 VSL Status : UP VSL Uptime : 3 minutes VSL Control Link : Gi2/4/45 

Additionally,  Example  1-16 illustrates how to verify information about the VSL port channel configuration using the **show switch virtual link port-channel** command. 

**Example 1-16** _Display the Virtual Switch Domain Number_ 

SW1# **sh switch virtual link port-channel** Executing the command on VSS member switch role = VSS Active, id = 1 Flags: D - down       P - bundled in port-channel I - stand-alone s - suspended H - Hot-standby (LACP only) R - Layer3     S - Layer2 U - in use     N - not in use, no aggregation f - failed to allocate aggregator M - not in use, no aggregation due to minimum links not met m - not in use, port not aggregated due to minimum links not met u - unsuitable for bundling d - default port w - waiting to be aggregated Group Port-channel Protocol   Ports ------+-------------+-----------+------------------5     Po5(SU)          -       Gi1/7/3(P) Gi1/7/4(P) 10    Po10(SU)         -       Gi2/4/45(P) Gi2/4/46(P) Executing the command on VSS member switch role = VSS Standby, id = 2 Flags: D - down       P - bundled in port-channel 

38  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

I - stand-alone s - suspended H - Hot-standby (LACP only) R - Layer3     S - Layer2 U - in use     N - not in use, no aggregation f - failed to allocate aggregator M - not in use, no aggregation due to minimum links not met m - not in use, port not aggregated due to minimum links not met u - unsuitable for bundling d - default port w - waiting to be aggregated Group Port-channel Protocol   Ports ------+-------------+-----------+------------------5     Po5(SU)          -       Gi1/7/3(P) Gi1/7/4(P) 10    Po10(SU)         -       Gi2/4/45(P) Gi2/4/46(P) SW1#

## **IOS-XE** 

In the twenty-first century, we find ourselves dealing with the ever-evolving needs of a modern network, meaning a network with the capacity to support varied and intelligent management tools as well as software-defined network mechanisms that rapidly exceed the capacity of the traditional Internetworking Operating System (IOS). This has resulted largely because of the monolithic nature of IOS itself. 

We first have to recognize that IOS has served us well over the years, but now the demands of networks have forced us to relook at how we support the operational process of typical protocols like OSPF, EIGRP, MPLS, BGP, and IPv6, to name a few. So it should come as no surprise that in an effort to expand the serviceability and survivability of IOS, it was necessary for it to evolve as well. In fact, IOS has evolved into three primary operating systems that each service and fulfill different purposes in the grand scheme of the network. These operation systems include variants like NX-OS, IOS-XR, and IOS-XE. Of these, the one we will concern ourselves with is IOS-XE. 

It should go without saying that IOS-XE was designed for routers, switches, and appliances, and as such, it embraces all the field-tested capabilities and features of IOS, while adding new functionality and benefits traditionally found in a portable operating system interface (POSIX) environment. This was the most logical approach available to integrate network-aware applications into modern routing devices. As a result, IOS-XE seamlessly integrates a generic approach to network management into every function, borrowing heavily from the equally reliable POSIX operating system. Furthermore, through the incorporation of a series of well-defined application programming interfaces (API), Cisco has improved IOS portability. Specifically, we are making reference to the operation of 

Chapter 1: Ethernet Basics  39 

IOS across platforms as well as extending capabilities outside of IOS. This final component to IOS-XE creates a future where application integration will be simplified, integral, and commonplace. 

IOS has been the center point for network expansion, configuration, and operation for decades, and this same functionality is now integrated into IOS-XE, thus preserving all the advantages of traditional IOS and its unparalleled history for delivering functionality for business-critical applications. All of this is done while retaining the same look and feel of IOS, but doing it while ensuring enhanced “future-proof” functionality. 

How is all this possible? IOS-XE runs a modern Linux operating system that employs a single daemon; the additional functionality we have been discussing will be run as isolated processes within the OS of the host. This means that we have all the capabilities we had in IOS with enhanced operations and functionality that will not require retraining. 

At first glance, this might not seem to be that big of an improvement, but if we keep in mind that running IOS and these other applications as separate processes, it becomes apparent that we can now leverage symmetrical multiprocessing. This in itself means that we can garner the benefits of load balancing across multiple-core CPUs by binding processes to different cores. Thus, we create an operational environment where it is possible to support multithreading and multicore CPUs. This capability, coupled with how IOS-XE separates the control plane from the forwarding plane, ensures a level of management and control that could not possibly exist in the context of the traditional monolithic IOS. 

Today, the IOS that runs on routers runs all the necessary modules to perform network operations in the same memory space. This is problematic if something were to happen to the routing engine because the result would be that the entire IOS kernel could crash. As early as five years ago, this might have been a tenable situation, but in the modern enterprise this is catastrophic, because today’s business networks running virtualizationenabled infrastructures consolidated on single platforms cannot allow a single process to bring down an entire assembly. 

By moving the software architecture to a system daemon running on a “Linux platform,” we now have the multiple levels of abstraction. The overall result is now inside of IOS-XE individual system functions that have been isolated from the primary operation kernel by placing them into separate processes. This means that should one of these isolated processes fail, it will not affect the kernel. So the idea of symmetrical multiprocessing gets taken one step further now by creating individual threads for each underlying process we have on our routing devices. 

It is through this isolated operation model that application designers will have the ability to build drivers for new data plane ASICs and have them interoperate with sets of standard APIs. It is these APIs that will then create control plane and data plane processing separation. 

It has been customary for some time to describe the operation mechanism of a router as falling into one or more different categories. Specifically, we are referring to the control plane, the data plane, and the input/output plane. The capability of an operating system to isolate the operation mechanisms of these three planes has a direct impact on device uptime as it relates to planned or unplanned outages. 

40  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

As a result of the modular architecture that we have attributed to IOS-XE, we see both **Key** a logical and a physical isolation of the control and data planes themselves. This at first **Topic** might seem to be a subtle difference, but in fact, this has far-reaching benefits. Now we have physical separation of the three planes through modular blades that are installed into the chassis, each having dedicated hardware resources. IOS-XE also maintains logical separation as an abstraction layer. We get even more capabilities to reduce failure domains within the routing system, as well as the capability to isolate operation loads between planes. An example of this would be heavy stress caused by forwarding massive amounts of traffic in the data plane, which would have no impact on the control plane running on the same chassis. This is made possible by the fact that IOS-XE runs a separate driver instance for each bay or blade slot in the chassis; therefore, one drive failing will have no impact on the other bays or the chassis as a whole. The outcome is that all the other processes will continue to forward traffic. In addition to this, we can actually patch individual drivers without bringing down the entire chassis. 

This separation is achieved through the Forwarding and Feature Manager (FFM) and the Forwarding Engine Driver (FED). 

The FFM provides a set of APIs used to manage the control plane processes. The resulting outcome is that the FFM programs the data plane through the FED and maintains all forwarding states for the system. It is the FED that allows the drivers to affect the data plane, and it is provided by the platform. 

Chapter 1: Ethernet Basics  41

## **Foundation Summary** 

This section lists additional details and facts to round out the coverage of the topics in this chapter. Unlike most of the Cisco Press Exam Certification Guides, this “Foundation Summary” does not repeat information presented in the “Foundation Topics” section of the chapter. Please take the time to read and study the details in the “Foundation Topics” section of the chapter, as well as review items noted with a Key Topic icon. 

Table  1-8 lists the different types of Ethernet and some distinguishing characteristics of each type. 

**Table 1-8** _Ethernet Standards_ 

|**Table 1-8** _Etherne_|_t Standards_|
|---|---|
|**Type of Ethernet**|**General Description**|
|10BASE5|Commonly called “Thicknet”; uses coaxial cabling|
|10BASE2|Commonly called “Thinnet”; uses coaxial cabling|
|10BASE-T|First type of Ethernet to use twisted-pair cabling|
|DIX Ethernet|Layer 1 and Layer 2 specifications for original Ethernet, from Digital/|
|Version 2|Intel/Xerox; typically called DIX V2|
|IEEE 802.3|Called MAC because of the name of the IEEE committee (Media|
||Access Control); original Layer 1 and 2 specifications, standardized|
||using DIX V2 as a basis|
|IEEE 802.2|Called LLC because of the name of the IEEE committee (Logical Link|
||Control); Layer 2 specification for headers common to multiple IEEE|
||LAN specifications|
|IEEE 802.3u|IEEE standard for Fast Ethernet (100 Mbps) over copper and optical|
||cabling; typically called FastE|
|IEEE 802.3z|Gigabit Ethernet over optical cabling; typically called GigE|
|IEEE 802.3ab|Gigabit Ethernet over copper cabling|



Switches forward frames when necessary, and do not forward when there is no need to do so, thus reducing overhead. To accomplish this, switches perform three actions: 

- Learn MAC addresses by examining the source MAC address of each received frame 

- Decide when to forward a frame or when to filter (not forward) a frame, based on the destination MAC address 

- Create a loop-free environment with other bridges by using the Spanning Tree Protocol 

The internal processing algorithms used by switches vary among models and vendors; regardless, the internal processing can be categorized as one of the methods listed in Table  1-9 . 

42  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 1-9** _Switch Internal Processing_ 

|**Switching**|**Description**|
|---|---|
|**Method**||
|Store-and-forward|The switch fully receives all bits in the frame (store) before forwarding|
||the frame (forward). This allows the switch to check the frame check|
||sequence (FCS) before forwarding the frame, thus ensuring that|
||errored frames are not forwarded.|
|Cut-through|The switch performs the address table lookup as soon as the|
||Destination Address field in the header is received. The first bits in the|
||frame can be sent out the outbound port before the final bits in the|
||incoming frame are received. This does not allow the switch to discard|
||frames that fail the FCS check, but the forwarding action is faster,|
||resulting in lower latency.|
|Fragment-free|This performs like cut-through switching, but the switch waits for 64|
||bytes to be received before forwarding the first bytes of the outgoing|
||frame. According to Ethernet specifications, collisions should be|
||detected during the first 64 bytes of the frame, so frames that are in|
||error because of a collision will not be forwarded.|



Table  1-10 lists some of the most popular Cisco IOS commands related to the topics in this chapter. 

**Table 1-10** _Catalyst IOS Commands for Catalyst Switch Configuration_ 

|**Command**|**Description**|
|---|---|
|**interface vlan 1**|Global command; moves user to interface|
||configuration mode for a VLAN interface|
|**interface fastethernet ** _0/x_|Puts user in interface configuration mode for|
||that interface|
|**duplex **{**auto **|**full **|**half**}|Used in interface configuration mode; sets|
||duplex mode for the interface|
|**speed **{**10 **|**100 **|**1000 **|**auto **||Used in interface configuration mode; sets|
|**nonegotiate**}|speed for the interface|
|**show mac address-table **[**aging-time **||Displays the MAC address table; the security|
|**count **|**dynamic **|**static**] [**address ** _hw-addr_]|option displays information about the|
|[**interface ** _interface-id_] [**vlan ** _vlan-id_]|restricted or static settings|
|**show interface fastethernet 0/ **_x_|Displays interface status for a physical 10/100|
||interface|
|**show interface vlan 1**|Displays IP address configuration for a VLAN|
|**remote span**|In VLAN configuration mode, specifies that|
||the VLAN is configured as a remote SPAN|
||destination VLAN|



Chapter 1: Ethernet Basics  43 

|**Command**|**Description**|
|---|---|
|**monitor session ** _1-66_ **source **[**vlan ** _vlan-id_|Configures a SPAN or RSPAN source, which|
||**interface ** _interface-id_] [**rx **|**tx **|**both**]|can include one or more physical interfaces|
||or one or more VLANs; optionally specifies|
||traffic entering (Rx) or leaving (Tx), or both,|
||with respect to the specified source|
|**monitor session 1-66 destination **[**remote**|Configures the destination of a SPAN or|
|**vlan ** _vlan-id_] |**interface ** _interface-id_]|RSPAN session to be either a physical interface|
||or a remote VLAN|
|**monitor session ** _1-66_ **filter vlan **[_vlan_||Removes traffic from the specified VLAN or|
|_vlan-range_]|VLAN range from the monitored traffic stream|
|**show monitor session ** _session-id_|Displays the status of a SPAN session|



Table  1-11 outlines the types of UTP cabling. 

**Table 1-11** _UTP Cabling Reference_ 

|**UTP**|**Max Speed**|**Description**|
|---|---|---|
|**Category**|**Rating**||
|1|—|Used for telephones and not for data|
|2|4 Mbps|Originally intended to support Token Ring over UTP|
|3|10 Mbps|Can be used for telephones as well; popular option for Ethernet|
|||in years past, if Cat 3 cabling for phones was already in place|
|4|16 Mbps|Intended for the fast Token Ring speed option|
|5|1 Gbps|Very popular for cabling to the desktop|
|5e|1 Gbps|Added mainly for the support of copper cabling for Gigabit|
|||Ethernet|
|6|1 Gbps+|Intended as a replacement for Cat 5e, with capabilities to|
|||support multigigabit speeds|



Table  1-12 lists the pertinent details of the Ethernet standards and the related cabling. 

44  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 1-12** _Ethernet Types and Cabling Standards_ 

|**Standard**|**Cabling**|**Maximum Single Cable Length**|
|---|---|---|
|10BASE5|Thick coaxial|500 m|
|10BASE2|Thin coaxial|185 m|
|10BASE-T|UTP Cat 3, 4, 5, 5e, 6|100 m|
|100BASE-FX|Two strands, multimode|400 m|
|100BASE-T|UTP Cat 3, 4, 5, 5e, 6, 2 pair|100 m|
|100BASE-T4|UTP Cat 3, 4, 5, 5e, 6, 4 pair|100 m|
|100BASE-TX|UTP Cat 3, 4, 5, 5e, 6, or STP, 2 pair|100 m|
|1000BASE-LX|Long-wavelength laser, MM or SM|10 km (SM)|
||fiber|3 km (MM)|
|1000BASE-SX|Short-wavelength laser, MM fiber|220 m with 62.5-micron fiber;|
|||550 m with 50-micron fiber|
|1000BASE-ZX|Extended wavelength, SM fiber|100 km|
|1000BASE-CS|STP, 2 pair|25 m|
|1000BASE-T|UTP Cat 5, 5e, 6, 4 pair|100 m|

## **Memory Builders** 

The CCIE Routing and Switching written exam, like all Cisco CCIE written exams, covers a fairly broad set of topics. This section provides some basic tools to help you exercise your memory about some of the broader topics covered in this chapter.

## **Fill In Key Tables from Memory** 

Appendix  E , “Key Tables for CCIE Study,” on the CD in the back of this book, contains empty sets of some of the key summary tables in each chapter. Print  Appendix  E , refer to this chapter’s tables in it, and fill in the tables from memory. Refer to  Appendix  F , “Solutions for Key Tables for CCIE Study,” on the CD to check your answers.

## **Definitions** 

Next, take a few moments to write down the definitions for the following terms: 

Autonegotiation, half duplex, full duplex, crossover cable, straight-through cable, unicast address, multicast address, broadcast address, loopback circuitry, I/G bit, U/L bit, CSMA/CD, SPAN, RSPAN, ERSPAN, remote VLAN, monitor session, VLAN filtering, encapsulation replication, VSS, VSL, FED, FFM 

Refer to the glossary to check your answers. 

Chapter 1: Ethernet Basics  45

## **Further Reading** 

For a good reference for more information on the actual FLPs used by autonegotiation, refer to the Fast Ethernet web page of the University of New Hampshire Research Computing Center’s InterOperability Laboratory, at  www.iol.unh.edu/services/testing/fe/ training/ . 

For information about configuring SPAN and RSPAN, and for a full set of restrictions (specific to the 3560 and 3750), see  www.ciscosystems.com/en/US/docs/switches/lan/ catalyst3560/software/release/12.2_50_se/configuration/guide/swspan.html . 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0087-00.png)

## **Blueprint topics covered in this chapter:** 

This chapter covers the following subtopics from the Cisco CCIE Routing and Switching written exam blueprint. Refer to the full blueprint in Table I-1 in the Introduction for more details on the topics covered in each chapter and their context within the blueprint. 

- VLANs 

- VLAN Trunking 

- VLAN Trunking Protocol (VTP) 

- PPP over Ethernet (PPPoE)

## **CHAPTER 2**

## **Virtual LANs and VLAN Trunking** 

This chapter continues with the coverage of some of the most fundamental and important LAN topics with coverage of VLANs and VLAN trunking. As usual, for those of you current in your knowledge of the topics in this chapter, review the items next to the Key Topic icons spread throughout the chapter, plus the “Foundation Summary” and “Memory Builders” sections at the end of the chapter.

## **“Do I Know This Already?” Quiz** 

Table  2-1 outlines the major headings in this chapter and the corresponding “Do I Know This Already?” quiz questions. 

**Table 2-1** _“Do I Know This Already?” Foundation Topics Section-to-Question Mapping_ 

|**Table 2-1** _“Do I Know This Alrea_|_dy?” Foundation Topics Section-to-Questio_|_n Mapping_|
|---|---|---|
|**Foundation Topics Section**|**Questions Covered in This Section**|**Score**|
|Virtual LANs|1–2||
|VLAN Trunking Protocol|3–5||
|VLAN Trunking: ISL and 802.1Q|6–9||
|Configuring PPPoE|10||
|**Total Score**|||



To best use this pre-chapter assessment, remember to score yourself strictly. You can find the answers in  Appendix  A , “Answers to the ‘Do I Know This Already?’ Quizzes.” 

**1.** Assume that VLAN 28 does not yet exist on Switch1. Which of the following commands, issued in the global configuration mode (reached with the **configure terminal** command) or any of its submodes would cause the VLAN to be created? 

   - **a. vlan 28** 

   - **b. vlan 28 name fred** 

   - **c. switchport vlan 28** 

   - **d. switchport access vlan 28** 

   - **e. switchport access 28** 

48  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**2.** Which of the following are advantages of using Private VLANs? 

   - **a.** Better LAN security 

   - **b.** IP subnet conservation 

   - **c.** Better consistency in VLAN configuration details 

   - **d.** Reducing the impact of broadcasts on end-user devices 

   - **e.** Reducing the unnecessary flow of frames to switches that do not have any ports in the VLAN to which the frame belongs 

**3.** Which of the following VLANs can be pruned by VTP on an 802.1Q trunk? 

   - **a.** 1–1023 

   - **b.** 1–1001 

   - **c.** 2–1001 

   - **d.** 1–1005 

   - **e.** 2–1005 

**4.** An existing switched network has ten switches, with Switch1 and Switch2 being the only VTPv2 servers in the network. The other switches are all VTPv2 clients and have successfully learned about the VLANs from the VTPv2 servers. The only configured VTP parameter on all switches is the VTP domain name (Larry). The VTP revision number is 201. What happens when a new, already-running VTPv2 client switch, named Switch11, with domain name Larry and revision number 301, connects through a trunk to any of the other ten switches? 

   - **a.** No VLAN information changes; Switch11 ignores the VTP updates sent from the two existing VTP servers until the revision number reaches 302. 

   - **b.** The original ten switches replace their old VLAN configuration with the configuration in Switch11. 

   - **c.** Switch11 replaces its own VLAN configuration with the configuration sent to it by one of the original VTP servers. 

   - **d.** Switch11 merges its existing VLAN database with the database learned from the VTP servers, because Switch11 had a higher revision number. 

Chapter 2: Virtual LANs and VLAN Trunking  49 

**5.** An existing switched network has ten switches, with Switch1 and Switch2 being the only VTPv3 servers in the network, and Switch1 being the primary server. The other switches are all VTPv3 clients, and have successfully learned about the VLANs from the VTP server. The only configured VTP parameter is the VTP domain name (Larry). The VTP revision number is 201. What happens when an already-running VTPv3 server switch, named Switch11, with domain name Larry and revision number 301, connects through a trunk to any of the other ten switches? 

   - **a.** No VLAN information changes; all VTP updates between the original VTP domain and the new switch are ignored. 

   - **b.** The original ten switches replace their old VLAN configuration with the configuration in Switch11. 

   - **c.** Switch11 replaces its old VLAN configuration with the configuration sent to it by one of the original VTP servers. 

   - **d.** Switch11 merges its existing VLAN database with the database learned from the VTP servers, because Switch11 had a higher revision number. 

   - **e.** None of the other answers is correct. 

**6.** Assume that two brand-new Cisco switches were removed from their cardboard boxes. PC1 was attached to one switch, PC2 was attached to the other, and the two switches were connected with a cross-over cable. The switch connection dynamically formed an 802.1Q trunk. When PC1 sends a frame to PC2, how many additional bytes of header are added to the frame before it passes over the trunk? 

   - **a.** 0 

   - **b.** 4 

   - **c.** 8 

   - **d.** 26 

**7.** Assume that two brand-new Cisco Catalyst 3560 switches were connected with a cross-over cable. Before the cable was attached, one switch interface was configured with the **switchport trunk encapsulation dot1q** , **switchport mode trunk** , and **switchport nonegotiate** subcommands. Which of the following must be configured on the other switch before trunking will work between the switches? 

   - **a. switchport trunk encapsulation dot1q** 

   - **b. switchport mode trunk** 

   - **c. switchport nonegotiate** 

   - **d.** No configuration is required. 

50  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**8.** When configuring trunking on a Cisco router Fa0/1 interface, under which configuration modes could the IP address associated with the native VLAN (VLAN 1 in this case) be configured? 

   - **a.** Interface Fa0/1 configuration mode 

   - **b.** Interface Fa0/1.1 configuration mode 

   - **c.** Interface Fa0/1.2 configuration mode 

   - **d.** None of the other answers is correct. 

**9.** Which of the following about 802.1Q are false? 

   - **a.** Encapsulates the entire frame inside an 802.1Q header and trailer 

   - **b.** Has a concept of a native VLAN 

   - **c.** Allows VTP to operate only on extended-range VLANs 

   - **d.** Is chosen over ISL by DTP 

**10.** Which command enables PPPoE client functionality on the outside Ethernet interface on a Cisco router? 

   - **a. pppoe enable** 

   - **b. pppoe-client enable** 

   - **c. pppoe-client dialer-pool-number** 

   - **d. pppoe-client dialer-number** 

Chapter 2: Virtual LANs and VLAN Trunking  51 

**Key Topic**

## **Foundation Topics**

## **Virtual LANs** 

In an Ethernet LAN, a set of devices that receive a broadcast sent by any one of the devices in the same set is called a _broadcast domain_ . On switches that have no concept of virtual LANs (VLAN), a switch simply forwards all broadcasts out all interfaces, except the interface on which it received the frame. As a result, all the interfaces on an individual switch are in the same broadcast domain. Also, if the switch connects to other switches and hubs, the interfaces on those switches and hubs are also in the same broadcast domain. 

A _VLAN_ is simply an administratively defined subset of switch ports that are in the same broadcast domain. Ports can be grouped into different VLANs on a single switch, and on multiple interconnected switches as well. By creating multiple VLANs, the switches create multiple, yet contained, broadcast domains. By doing so, a broadcast sent by a device in one VLAN is forwarded to the other devices in that same VLAN; however, the broadcast is not forwarded to devices in the other VLANs. 

With VLANs and IP, best practices dictate a one-to-one relationship between VLANs and IP subnets. Simply put, the devices in a single VLAN are typically also in the same single IP subnet. Alternately, it is possible to put multiple subnets in one VLAN, and use secondary IP addresses on routers to route between the VLANs and subnets. Ultimately, the CCIE written exams tend to focus more on the best use of technologies, so this book will assume that one subnet sits on one VLAN, unless otherwise stated. 

Layer 2 switches forward frames between devices in the same VLAN, but they do not forward frames between two devices in different VLANs. To forward data between two VLANs, a multilayer switch (MLS) or router is needed.  Chapter  6 , “IP Forwarding (Routing),” covers the details of MLS.

## **VLAN Configuration** 

On Cisco IOS–based switches, a VLAN is primarily identified by its numerical ID, which is the only mandatory argument when creating, modifying, or deleting a VLAN. A VLAN can be assigned a verbal name for better orientation, but only a very few places in the CLI allow substituting the VLAN name for its ID. Also, a VLAN has an operational state: It can either be _active_ , which is the default state, or it can be _suspended_ . A suspended VLAN is hibernated—while it exists, it does not operate. Access ports in a suspended VLAN are unable to communicate and drop all frames, similar to ports put into a nonexistent VLAN. Putting a suspended VLAN back into the active state also reinstates normal communication on all ports in that VLAN. 

52  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Configuring VLANs in a network of Cisco switches requires just a few simple steps: 

**Step 1.** Create the VLAN itself, optionally configuring its name and state. 

**Step 2.** Associate the correct ports with that VLAN. 

The challenge relates to how some background tasks differ depending on how the Cisco _VLAN Trunking Protocol (VTP)_ is configured, and whether normal-range or extendedrange VLANs are being used. We will discuss VTP and VLAN ranges in more detail later in this chapter.

## Using VLAN Database Mode to Create VLANs 

To begin, consider  Example  2-1 , which shows some of the basic mechanics of VLAN creation in _VLAN database configuration mode_ . While this configuration mode is considered obsolete on recent switches and might not be supported at all, it might still be used on older Catalyst platforms and on ISR and ISR G2 routers with switching modules installed. VLAN database configuration mode allows the creation of VLANs, basic administrative settings for each VLAN, and verification of VTP configuration information. Only normal-range (VLANs 1–1005) VLANs can be configured in this mode, and the VLAN configuration is stored in a Flash file called vlan.dat. In general, the _VLAN database configuration mode_ should be avoided if possible, and hopefully you will not need to use it anymore; however, there are still switches and even relatively recent routers deployed in networks that do not support the newer way of configuring VLANs in global configuration mode. 

Example  2-1 demonstrates VLAN database configuration mode, showing the configuration on Switch3 from  Figure  2-1 . The example shows VLANs 21 and 22 being created. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0093-08.png)


**----- Start of picture text -----**<br>
VLAN 21 VLAN 22<br>Subnet 10.1.21.x/24 Subnet 10.1.22.x/24<br>Fa0/0 Fa0/1 Gi0/1 Fa0/2<br>R1 SW1 SW2 R2<br>Fa0/12 Fa0/24<br>Fa0/3<br>R3 SW3 SW4<br>Fa0/7 Fa0/5<br>PC1<br>R4<br>**----- End of picture text -----**<br>


**Figure 2-1** _Simple Access and Distribution_ 

Chapter 2: Virtual LANs and VLAN Trunking  53 

**Key Topic** 

**Example 2-1** _VLAN Creation in VLAN Database Mode – Switch3_ 

~~! Below, note that Fa0/12 and Fa0/24 are missing from the list, because they have ! dynamically become trunks, supporting multiple VLANs. Switch3#~~ ~~**show vlan brief**~~ VLAN Name                             Status    Ports ---- -------------------------------- --------- ------------------------------1    default                          active    Fa0/1, Fa0/2, Fa0/3, Fa0/4 Fa0/5, Fa0/6, Fa0/7, Fa0/8 Fa0/9, Fa0/10, Fa0/11, Fa0/13 Fa0/14, Fa0/15, Fa0/16, Fa0/17 Fa0/18, Fa0/19, Fa0/20, Fa0/21 Fa0/22, Fa0/23 ~~! Below, "unsup" means that this 2950 switch does not support FDDI and TR~~ 1002 fddi-default                     act/unsup 1003 token-ring-default               act/unsup 1004 fddinet-default                  act/unsup 1005 trnet-default                    act/unsup ~~! Below,~~ ~~**vlan database** moves user to VLAN database configuration mode. ! The~~ ~~**vlan 21** command defines the VLAN, as seen in the next command output ! (~~ ~~**show current** ), VLAN 21 is not in the "current" VLAN list. Switch3#~~ ~~**vlan database**~~ Switch3(vlan)# **vlan 21** ~~VLAN 21 added: Name: VLAN0021 ! The~~ ~~**show current** command lists the VLANs available to the IOS when the switch ! is in VTP Server mode. The command lists the VLANs in numeric order, with ! VLAN 21 missing.~~ 

Switch3(vlan)# **show current** ~~VLAN ISL Id: 1~~ Name: default Media Type: Ethernet VLAN 802.10 Id: 100001 State: Operational MTU: 1500 Backup CRF Mode: Disabled Remote SPAN VLAN: No 

54  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

~~! Lines omitted for brevity~~ 

~~! Next, note that~~ ~~**show proposed** lists VLAN 21. The~~ ~~**vlan 21** command~~ 

~~! creates the definition, but it must be "applied" before it is "current".~~ 

Switch3(vlan)# **show proposed** VLAN ISL Id: 1 Name: default Media Type: Ethernet VLAN 802.10 Id: 100001 State: Operational MTU: 1500 Backup CRF Mode: Disabled Remote SPAN VLAN: No 

~~VLAN ISL Id: 21~~ 

Name: VLAN0021 Media Type: Ethernet VLAN 802.10 Id: 100021 State: Operational MTU: 1500 Backup CRF Mode: Disabled Remote SPAN VLAN: No 

~~! Lines omitted for brevity~~ 

~~! Next, you could~~ ~~**apply** to complete the addition of VLAN 21,~~ 

~~!~~ ~~**abort** to not make the changes and exit VLAN database mode, or~~ 

~~!~~ ~~**reset** to not make the changes but stay in VLAN database mode.~~ 

Switch3(vlan)# **?** 

VLAN database editing buffer manipulation commands: 

~~abort  Exit mode without applying the changes apply  Apply current changes and bump revision number~~ exit   Apply changes, bump revision number, and exit mode no     Negate a command or set its defaults ~~reset  Abandon current changes and reread current database~~ show   Show database information vlan   Add, delete, or modify values associated with a single VLAN vtp    Perform VTP administrative functions. 

~~! The~~ ~~**apply** command was used, making the addition of VLAN 21 complete.~~ 

Switch3(vlan)# **apply** ~~APPLY completed.~~ 

Chapter 2: Virtual LANs and VLAN Trunking  55 

~~! A~~ ~~**show current** now would list VLAN 21.~~ 

~~Switch3(vlan)#~~ ~~**vlan 22 name ccie-vlan-22** VLAN 22 added: Name: ccie-vlan-22 ! Above and below, some variations on commands are shown, along with the ! creation of VLAN 22, with name~~ ~~_ccie-vlan-22_ . ! Below, the~~ ~~**vlan 22** option is used on~~ ~~**show current** and~~ ~~**show proposed** ! detailing the fact that the apply has not been done yet. Switch3(vlan)#~~ ~~**show current 22** VLAN 22 does not exist in current database Switch3(vlan)#~~ ~~**show proposed 22** VLAN ISL Id: 22~~ 

- ~~! Lines omitted for brevity ! Finally, the user exits VLAN database mode using CTRL-Z, which does !~~ ~~**not** inherently apply the change. CTRL-Z actually executes an~~ ~~**abort** . Switch3(vlan)# ^Z~~

## Using Configuration Mode to Put Interfaces into VLANs 

To put a VLAN to use, the VLAN must be created, and then switch ports must be assigned to the VLAN.  Example  2-2 shows how to associate the interfaces with the correct VLANs, once again on Switch3. 

**Note** At the end of Example 2-1, VLAN 22 had not been successfully created. The assumption for Example 2-2, however, is that VLAN 22 has been successfully created.

## **Example 2-2** _Assigning Interfaces to VLANs – Switch3_ 

**Key Topic** 

~~! First, the~~ ~~**switchport mode access** command configures respective interfaces for~~ 

~~! static access mode, and the~~ ~~**switchport access vlan** command assigns them into~~ 

~~! respective VLANs.~~ Switch3# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. Switch3(config)# **int fa 0/3** Switch3(config-if)# **switchport mode access** ~~Switch3(config-if)#~~ ~~**switchport access vlan 22**~~ 

56  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Switch3(config-if)# **int fa 0/7** Switch3(config-if)# **switchport mode access** ~~Switch3(config-if)#~~ ~~**switchport access vlan 21**~~ Switch3(config-if)# **^Z** ~~! Below,~~ ~~**show vlan brief** lists these same two interfaces as now being in ! VLANs 21 and 22, respectively.~~ 

~~Switch3#~~ ~~**show vlan brief**~~ VLAN Name                             Status    Ports ---- -------------------------------- --------- ------------------------------1    default                          active    Fa0/1, Fa0/2, Fa0/4, Fa0/5 Fa0/6, Fa0/8, Fa0/9, Fa0/10 Fa0/11, Fa0/13, Fa0/14, Fa0/15 Fa0/16, Fa0/17, Fa0/18, Fa0/19 Fa0/20, Fa0/21, Fa0/22, Fa0/23 21   VLAN0021                         active    Fa0/7 22   ccie-vlan-22                     active    Fa0/3 ~~! Lines omitted for brevity ! While the VLAN configuration is not shown in the running-config at this point, ! the~~ ~~**switchport access** command that assigns the VLAN for the interface is in the ! configuration, as seen with the~~ ~~**show run int fa 0/3** command. Switch3#~~ ~~**show run int fa 0/3**~~ interface FastEthernet0/3 ~~switchport access vlan 22~~ switchport mode access

## Using Configuration Mode to Create VLANs 

At this point, the two new VLANs (21 and 22) have been created on Switch3, and the two interfaces are now in the correct VLANs. However, all recent Cisco IOS–based switches support a different way to create VLANs, using configuration mode, as shown in  Example  2-3 . This is the preferred mode for configuring VLANs whenever supported, and is the only mode that can be used to configure extended-range and Private VLANs. All VLAN settings are performed in the **vlan** _vlan-id_ mode accessed from global configuration level. Configuration changes apply only after exiting the **vlan** mode; this is one of the few IOS CLI contexts in which changes are not applied immediately after entering individual commands. 

Chapter 2: Virtual LANs and VLAN Trunking  57 

**Key Topic** 

**Example 2-3** _Creating VLANs in Configuration Mode – Switch3_ 

~~! First, VLAN 31 did not exist when the~~ ~~**switchport access vlan 31** command was ! issued. As a result, the switch both created the VLAN and put~~ ~~**interface fa0/8** ! into that VLAN. Then, the~~ ~~**vlan 32** global command was used to create a ! VLAN from configuration mode, and the~~ ~~**name** subcommand was used to assign a ! non-default name.~~ Switch3# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. Switch3(config)# **int fa 0/8** Switch3(config-if)# **switchport mode access** ~~Switch3(config-if)#~~ ~~**switchport access vlan 31** % Access VLAN does not exist. Creating vlan 31~~ Switch3(config-if)# **exit** Switch3(config)# **vlan 32** Switch3(config-vlan)# **name ccie-vlan-32** Switch3(config-vlan)# **^Z** ~~Switch3#~~ ~~**show vlan brief**~~ VLAN Name                             Status    Ports ---- -------------------------------- --------- ------------------------------1    default                          active    Fa0/1, Fa0/2, Fa0/4, Fa0/5 Fa0/6, Fa0/9, Fa0/10, Fa0/11 Fa0/13, Fa0/14, Fa0/15, Fa0/16 Fa0/17, Fa0/18, Fa0/19, Fa0/20 Fa0/21, Fa0/22, Fa0/23 21   VLAN0021                         active    Fa0/7 22   ccie-vlan-22                     active    Fa0/3 ~~31   VLAN0031                         active    Fa0/8 32   ccie-vlan-32                     active~~ ! Portions omitted for brevity 

Example  2-3 shows how the **switchport access vlan** subcommand creates the VLAN, as needed, and assigns the interface to that VLAN. Note that in  Example  2-3 , the **show vlan brief** output lists Fa0/8 as being in VLAN 31. Because no ports have been assigned to VLAN 32 as of yet, the final line in  Example  2-3 simply does not list any interfaces.

## Modifying the Operational State of VLANs 

The state of a VLAN—active or suspended—can be manipulated both in **vlan database** and in configuration mode. A VLAN can be suspended in two ways: _globally_ in the entire VTP domain and _locally_ on a single switch without influencing its state through 

58  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

VTP on other switches. The **state suspend** command, valid both in **vlan database** and in configuration mode, is used to globally suspend a VLAN. Suspending a VLAN locally, also called “locally shutting down the VLAN,” is accomplished using the **shutdown** command, and is supported only in the configuration mode in the VLAN context. Do not confuse the **shutdown** command in the VLAN context with the same command available under **interface Vlan** mode, which has a different and unrelated meaning (shutting down an SVI without further impairing the operation of the corresponding VLAN itself). Global and local VLAN states can be configured independently, but for a VLAN to be operational on a switch, it must be both globally and locally activated. Manipulating the operational state of VLANs and the use of corresponding commands are shown in greater detail in  Example  2-4 . 

**Example 2-4** _Modifying the Operational State of VLANs_ 

~~! First, put the VLAN 21 to global suspended state in~~ ~~**vlan database** mode. The state ! will be propagated by VTP to all switches in the VTP domain if VTP is used.~~ Switch3# **vlan database** Switch3(vlan)# **vlan 21 state ?** active   VLAN Active State suspend  VLAN Suspended State Switch3(vlan)# **vlan 21 state suspend** VLAN 31 modified: State SUSPENDED Switch3(vlan)# **exit** APPLY completed. Exiting.... ~~! VLAN 21 will now be listed as suspended~~ Switch3# **show vlan brief** VLAN Name                             Status    Ports ---- -------------------------------- --------- ------------------------------1    default                          active    Fa0/1, Fa0/2, Fa0/4, Fa0/5 Fa0/6, Fa0/9, Fa0/10, Fa0/11 Fa0/13, Fa0/14, Fa0/15, Fa0/16 Fa0/17, Fa0/18, Fa0/19, Fa0/20 Fa0/21, Fa0/22, Fa0/23 21   VLAN0021                         suspended Fa0/7 ~~! Portions omitted for brevity ! Now use the configuration mode to reactivate the VLAN~~ 

Chapter 2: Virtual LANs and VLAN Trunking  59 

Switch3# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. Switch3(config)# **vlan 21** Switch3(config-vlan)# **state active** Switch3(config-vlan)# **exit** Switch3(config)# **do show vlan brief** VLAN Name                             Status    Ports ---- -------------------------------- --------- ------------------------------1    default                          active    Fa0/1, Fa0/2, Fa0/4, Fa0/5 Fa0/6, Fa0/9, Fa0/10, Fa0/11 Fa0/13, Fa0/14, Fa0/15, Fa0/16 Fa0/17, Fa0/18, Fa0/19, Fa0/20 Fa0/21, Fa0/22, Fa0/23 21   VLAN0021                         active    Fa0/7 

~~! Portions omitted for brevity~~ 

~~! To locally suspend a VLAN, enter its configuration context and issue~~ 

~~! the~~ ~~**shutdown** command, then exit. Alternatively, you may also use the~~ 

~~!~~ ~~**shutdown vlan** global level configuration command that has exactly~~ 

~~! the same effect. In the VLAN listing, the VLAN 21 will be reported as~~ 

~~! active in the VTP domain on other switches, yet locally shutdown.~~ 

~~! It is also possible to both use the~~ ~~**state suspend** to suspend the VLAN~~ 

~~! via VTP globally, and~~ ~~**shutdown** to also have it locally shut down.~~ 

Switch3(config)# **vlan 21** Switch3(config-vlan)# **shutdown** Switch3(config-vlan)# **exit** Switch3(config)# **do show vlan brief** VLAN Name                             Status    Ports 

---- -------------------------------- --------- ------------------------------1    default                          active    Fa0/1, Fa0/2, Fa0/4, Fa0/5 Fa0/6, Fa0/9, Fa0/10, Fa0/11 Fa0/13, Fa0/14, Fa0/15, Fa0/16 Fa0/17, Fa0/18, Fa0/19, Fa0/20 Fa0/21, Fa0/22, Fa0/23 21   VLAN0021                         act/lshut Fa0/7 

! Portions omitted for brevity 

! To reactivate the locally shut VLAN, enter the **no shutdown** command in **vlan 21** 

! context, or more straightforward, enter the **no shutdown vlan 21** command 

Switch3(config)# **no shutdown vlan 21** Switch3(config)# **do show vlan brief** 

60  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

VLAN Name                             Status    Ports ---- -------------------------------- --------- ------------------------------1    default                          active    Fa0/1, Fa0/2, Fa0/4, Fa0/5 Fa0/6, Fa0/9, Fa0/10, Fa0/11 Fa0/13, Fa0/14, Fa0/15, Fa0/16 Fa0/17, Fa0/18, Fa0/19, Fa0/20 Fa0/21, Fa0/22, Fa0/23 21   VLAN0021                         active    Fa0/7 ! Portions omitted for brevity 

The VLAN creation process is simple but laborious in a large network. If many VLANs exist, and they exist on multiple switches, instead of manually configuring the VLANs on each switch, you can use VTP to distribute the VLAN configuration of a VLAN to the rest of the switches. VTP will be discussed later in the chapter.

## **Private VLANs** 

Engineers can design VLANs with many goals in mind. In many cases today, devices end up in the same VLAN just based on the physical locations of the wiring drops. Security is another motivating factor in VLAN design: Devices in different VLANs do not overhear each other’s broadcasts and possibly other communication. Additionally, the separation of hosts into different VLANs and subnets requires an intervening router or multilayer switch between the subnets, and these types of devices typically provide more robust security features. 

Regardless of the design motivations behind grouping devices into VLANs, good design practices typically call for the use of a single IP subnet per VLAN. In some cases, however, the need to increase security by separating devices into many small VLANs conflicts with the design goal of conserving the use of the available IP subnets. The Cisco Private VLAN feature described in RFC 5517 addresses this issue. Private VLANs allow a switch to separate ports as if they were on different VLANs, while consuming only a single subnet. 

A common place to implement Private VLANs is in the multitenant offerings of a service provider (SP). The SP can install a single router and a single switch. Then, the SP attaches devices from multiple customers to the switch. Private VLANs then allow the SP to use only a single subnet for the entire building, separating different customers’ switch ports so that they cannot communicate directly, while supporting all customers with a single router and switch. 

Conceptually, a Private VLAN is a mechanism that partitions a given VLAN into an **Key** arbitrary number of nonoverlapping sub-VLANs, or _secondary VLANs_ . This partition- **Topic** ing is invisible to the outside world that continues to see only the original VLAN, in this context called the _primary VLAN_ . An important consequence of this private partitioning is that from outside, the primary VLAN continues to use the same VLAN ID and IP subnet as the original VLAN. Internally, all secondary VLANs will share this common IP subnet, although each of them has a different, unique VLAN ID that is associated with 

Chapter 2: Virtual LANs and VLAN Trunking  61 

the primary VLAN. Hence, a Private VLAN can be described as a cluster of one or more secondary VLANs, represented to the outside by a single primary VLAN, not unlike a BGP confederation, where multiple internal sub-ASes are represented to external peers as a single AS. Consider the topology in  Figure  2-2 for an overview. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0102-02.png)


**----- Start of picture text -----**<br>
Promiscuous<br>Port Trunk<br>R1 192.168.100.254/24 SW1 SW2<br>Isolated<br>Community Community Community VLAN 199<br>VLAN 101 VLAN 102 VLAN 103<br>Primary VLAN 100<br>192.168.100.0/24<br>**----- End of picture text -----**<br>


**Figure 2-2** _Switched Network Utilizing Private VLANs_ 

Let us first consider the behavior of Private VLANs on a single switch. We will later discuss how the Private VLAN functionality extends to multiple switches over trunks. 

Secondary VLANs can be of two types: _community_ VLANs and _isolated_ VLANs. Ports assigned to the same community VLAN can communicate with each other directly, but they are not allowed to communicate with ports in any other VLAN. This behavior is similar to ordinary VLANs. A single primary VLAN can be associated with multiple community VLANs, each of them representing a group of devices that can talk directly to each other but that are separated from any other similar groups. 

On the other hand, ports assigned to an isolated VLAN can neither communicate with each other nor with ports in any other VLAN. A single primary VLAN can be associated with at most one isolated VLAN, as having multiple isolated VLANs under a single primary VLAN would make no sense. 

A single primary VLAN can be associated with zero or more community VLANs and with at most one isolated VLAN. A secondary VLAN, either a community or an isolated VLAN, must be associated with exactly one primary VLAN. 

As an example, consider a block of flats that needs to be fully networked, with you being the person responsible for configuring the networking equipment. A simple approach would be to connect all flats to a switch and assign all ports to a single VLAN, say, VLAN 100 utilizing the IP subnet 192.168.100.0/24. All stations in this VLAN share this IP space and can communicate with each other directly, and use a gateway IP address from the same subnet, for example, 192.168.100.254, to reach other networks. However, 

62  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

this network has an obvious security issue—users in individual flats are not controlled and cannot be trusted. A single misbehaving or infected computer in one flat can wreak havoc throughout the entire VLAN. Therefore, it is natural to require that individual flats be isolated from each other but still continue to use the former VLAN 100, the same IP subnet, and the same default gateway. This can be accomplished by creating a new _secondary isolated_ VLAN, for example, VLAN 199, associating it with the original VLAN 100 (thereby making the VLAN 100 a _primary_ VLAN) and assigning all access ports toward flats to the isolated VLAN 199. As a result, individual flats will be isolated from each other, yet they will continue to use the same IP address space and default gateway. The outside world will not see any difference. 

Life is seldom that simple, though. Selected users can start coming to you after a while and request direct visibility with other selected users because they want to mutually share files, stream a video, or play network games. There can be many similar groups of users that want to have mutual visibility, yet remain isolated from all other users. As an example, consider that three separate groups of users requesting mutual connectivity have formed in the block. Obviously, these groups form three communities, with members of each single community requesting full visibility with each other, yet keeping the separation between communities and from users that do not belong to any particular community. 

A comfortable way of solving this task is by creating three _secondary community_ VLANs, one for each community, and assigning each member of a single community to the same community VLAN. In this example, the first group can be assigned to community VLAN 101, the second group can be assigned to community VLAN 102, and the remaining group can be put into community VLAN 103. These secondary community VLANs 101–103 will be associated with the primary VLAN 100, again sharing its IP address space and default gateway. All other flats will remain in isolated VLAN 199 and will keep their total isolation. 

Depending on what secondary VLAN type a switch port is assigned to, we call these ports either _community ports_ or _isolated ports_ . In the preceding example, switch ports configured with VLANs 101–103 would be called community ports, while switch ports configured with VLAN 199 would be called isolated ports. Note that none of the ports mentioned so far is assigned to the primary VLAN 100. Both community and isolated ports behave as normal access ports—they technically belong to a single VLAN and they do not tag frames.

## **Key Topic** 

According to communication rules described so far, hosts in a particular community VLAN can only talk to other hosts in the same community VLAN and no one else; hosts in a particular isolated VLAN can talk to no one at all. There is, so far, no possibility of communicating with the world outside the given Private VLAN, nor a way of accessing common shared resources, such as network printers, storage, or servers. Clearly, the usefulness of such VLANs would be questionable at best. Therefore, there must be a way of defining a special port that is allowed to communicate with any member of any secondary VLAN under a particular primary VLAN. A device attached to such a port—a router, server, NAS, printer, and so on—would then be accessible by any host in any secondary VLAN under a particular primary VLAN, regardless of the type of the secondary VLAN. 

Chapter 2: Virtual LANs and VLAN Trunking  63 

**Key Topic** 

In Private VLAN terminology, such ports are called _promiscuous_ ports. A promiscuous port is not associated with any particular secondary VLAN. Instead, it is associated with the corresponding primary VLAN itself. A device connected to a promiscuous port can communicate with devices in all secondary VLANs associated with this primary VLAN and vice versa. A device in a secondary VLAN that is associated with a particular primary VLAN can communicate with any promiscuous port in that primary VLAN. If there are multiple promiscuous ports in the primary VLAN, they can also communicate with each other. Promiscuous ports also behave as access ports in the sense they do not use tagging. 

In the preceding example, if the default gateway 192.168.100.254 is an external router, it would be connected to a promiscuous port on the switch that implements the Private VLAN. This setup would allow hosts in VLANs 101–103 and 199 to communicate with other networks through this router. 

If Private VLANs are in use, the rules of communication on a single switch can be summarized as follows: 

- A port in a particular community VLAN (that is, a community port) can communicate with all other ports in the same community VLAN and with all promiscuous ports in the corresponding primary VLAN. 

- A port in a particular isolated VLAN (that is, an isolated port) can communicate with all promiscuous ports in the corresponding primary VLAN. 

- A port in a particular primary VLAN (that is, a promiscuous port) can communicate with all other promiscuous ports in the same primary VLAN and with all ports in all secondary VLANs associated with this primary VLAN. 

Extending the operation of Private VLANs over a set of switches is fairly simple. The basic goal is to increase the span of Private VLANs while keeping their defined behavior and containment. A port in a particular community VLAN shall be able to communicate with other ports in the same community VLAN and with all promiscuous ports in the corresponding primary VLAN on any switch. Similarly, a port in a particular isolated VLAN shall be able to communicate with all promiscuous ports in the corresponding primary VLAN on any switch. A promiscuous port in a particular primary VLAN shall be able to communicate with all other promiscuous ports in that primary VLAN and with all ports in all associated secondary VLANs on all switches. Because these requirements implicitly assume that a frame received on a port in a primary or secondary VLAN can be forwarded through trunk ports to other switches, yet another communication rule is hereby established: A frame received on a promiscuous, community, or isolated port can always be forwarded through a trunk port. 

Obviously, if all primary/secondary VLANs, their IDs, types, and associations are configured identically on all switches (provided they support the Private VLAN feature), each switch will give frames the same consistent treatment as soon as their membership in a particular VLAN is established. As frames between switches are carried by trunk ports, it is important to see how the tagging of frames received on a Private VLAN port is performed. 

64  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

If a frame is received on a community or isolated port and is forwarded through a trunk, the switch will tag the frame using the VLAN ID of the corresponding _secondary_ VLAN. The receiving switch will then forward the received frame further according to the type of the secondary VLAN. 

If a frame is received on a promiscuous port and is forwarded through a trunk, the switch will tag the frame using the VLAN ID of the corresponding _primary_ VLAN. The receiving switch will then forward the frame further as a frame coming from a promiscuous port. 

To summarize the communication and tagging rules in Private VLANs:

## **Key Topic** 

- A port in a particular community VLAN (that is, a community port) can communicate with all other ports in the same community VLAN, with all promiscuous ports in the corresponding primary VLAN, and with all trunks. 

- A port in a particular isolated VLAN (that is, an isolated port) can communicate with all promiscuous ports in the corresponding primary VLAN, and with all trunks. 

- A port in a particular primary VLAN (that is, a promiscuous port) can communicate with all other promiscuous ports in the same primary VLAN, with all ports in all secondary VLANs associated with this primary VLAN, and with all trunks. 

- A frame received on a community or isolated port will be tagged with the ID of the corresponding secondary VLAN when forwarded out a trunk. 

- A frame received on a promiscuous port will be tagged with the ID of the corresponding primary VLAN when forwarded out a trunk. 

- A frame received on a trunk tagged with a community or isolated VLAN ID will be forwarded as if it was received on a local community or isolated port in the corresponding secondary VLAN. 

- A frame received on a trunk tagged with a primary VLAN ID will be forwarded as if it was received on a local promiscuous port in the corresponding primary VLAN. 

- Community VLANs can be seen as VLANs carrying “upstream” traffic from a host to other hosts of the same community VLAN and to promiscuous ports in the corresponding primary VLAN. Isolated VLANs can be seen as VLANs carrying “upstream” traffic from hosts to promiscuous ports in the corresponding primary VLAN. A Primary VLAN can be seen as a VLAN carrying “downstream” traffic from promiscuous ports to other promiscuous ports and hosts in all associated secondary VLANs. 

Table  2-2 summarizes the communication rules between various ports. 

Chapter 2: Virtual LANs and VLAN Trunking  65 

**Table 2-2** _Private VLAN Communications Between Ports_ 

||**Table 2-2** _Private VLAN Communication_|_s Between Port_|_s_||
|---|---|---|---|---|
|**Key**|||||
|**Topic**|**Description of Who Can Talk to Whom**|**Primary**|**Community**|**Isolated**|
|||**VLAN Ports**|**VLAN Ports1**|**VLAN Ports1**|
||Talk to ports in primary VLAN|Yes|Yes|Yes|
||(promiscuous ports)||||
||Talk to ports in the same secondary VLAN|N/A2|Yes|No|
||(host ports)||||
||Talk to ports in another secondary VLAN|N/A2|No|No|
||Talk to trunks|Yes|Yes|Yes|



1 Community and isolated VLANs are secondary VLANs. 

2 Promiscuous ports, by definition in the primary VLAN, can talk to all other ports. 

There are two common misconceptions regarding the Private VLAN operation on trunks. The first misconception relates to the tagging. It is often incorrectly believed that Private VLANs use double tagging on trunks. This belief is supported by the apparent nesting of secondary VLANs inside their associated primary VLAN. In reality, secondary VLANs do not exist “inside” their primary VLAN; rather, they are only _associated_ with it. This association merely indicates that a frame received in a secondary VLAN can be forwarded out promiscuous ports in the associated primary VLAN and vice versa. 

The second misconception is related to trunk port types. We have so far described normal trunks ( **switchport mode trunk** ) that can be used both for ordinary and Private VLANs. There are, however, two special types of trunk ports with respect to Private VLANs. These special trunk port types are called Promiscuous PVLAN Trunk and Isolated PVLAN Trunk ports. Both these types _shall not be used_ in ordinary Private VLAN deployments between switches supporting Private VLANs; rather, their usage is limited to a set of special scenarios. To understand better, consider  Figure  2-3 , which contains a slightly modified topology, with VLAN 100 being the primary VLAN, VLANs 101 and 102 being community VLANs, and VLAN 199 being an isolated VLAN. In addition, there is VLAN 999, which spans the router and both switches and serves the purpose of a management VLAN. The SW1 switch is assumed to support Private VLANs while SW2 does not support them. 

The first special trunk type is the _Promiscuous PVLAN Trunk_ . Whenever a frame from a secondary VLAN is going to be sent out such a trunk, its VLAN tag will be rewritten with the appropriate primary VLAN ID. This rewriting is necessary when a trunk carrying a set of VLANs including Private VLANs is to be connected to an external device that does not support Private VLANs, yet which shall be reachable from the Private VLANs as if connected to a promiscuous port. If, for example, a router-on-stick like R1 in  Figure  2-3 is used to route between several VLANs including a primary VLAN, the external router does not understand that multiple secondary VLANs actually map to a single primary VLAN. The Promiscuous PVLAN Trunk port will translate all secondary VLAN IDs into the corresponding primary VLAN ID so that the external router always sees only the primary VLAN. 

66  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0107-01.png)


**----- Start of picture text -----**<br>
VLAN 100: Primary VLAN “Users” Promiscuous Isolated<br>VLAN 999: Management VLAN PVLAN Trunk PVLAN Trunk<br>SW1 SW2<br>R1<br>Isolated<br>Community Community VLAN 199<br>VLAN 101 VLAN 102<br>Primary VLAN 100<br>192.168.100.0/24<br>**----- End of picture text -----**<br>


**Figure 2-3** _Switched Topology Utilizing Special Trunk Types_ 

The second special type of a trunk is the _Isolated PVLAN Trunk_ . This trunk type translates a primary VLAN ID into the ID of the isolated VLAN that is associated with the primary VLAN. This is used to extend the isolated VLAN over a trunk carrying multiple VLANs to a switch that does not support Private VLANs but is capable of isolating its own ports. To illustrate, entry-level Catalyst switches do not support Private VLANs but they support so-called _protected_ ports (this feature is sometimes called the Private VLAN Edge). On these switches, a protected port can be configured using the **switchport protected** command. Protected ports configured with this command are prohibited from ever communicating with each other—in essence, they act just like isolated ports. If a frame is received on a promiscuous port in the primary PVLAN and is about to be sent out the Isolated PVLAN Trunk port, its VLAN tag currently carrying the primary VLAN ID will be rewritten to the isolated VLAN ID. If the neighboring switch has its protected ports assigned to the isolated VLAN (although the VLAN is not configured as isolated on that switch because it does not support Private VLANs), it will be able to forward the frame to the appropriate host. In  Figure  2-3 , the Isolated PVLAN Trunk is used to extend the isolated PVLAN 199 from SW1 to SW2 that does not support PVLANs, yet is capable of locally isolating its ports in VLAN 199. SW2 will not allow these ports to communicate together while allowing them to communicate with the trunk toward SW1. SW1 will make sure that a frame received on another isolated port in VLAN 199 will not be forwarded out the isolated PVLAN trunk toward SW2, and that a frame tagged with VLAN 199 coming through the isolated PVLAN trunk from SW2 will not be forwarded out any other isolated port in the same secondary VLAN. This way, the isolated secondary VLAN is extended to SW2 without losing any of its isolated properties. Should, however, R1 or any other device on a promiscuous port send a packet to a station on SW2, this packet would ordinarily be tagged with primary VLAN 100. On the isolated PVLAN 

Chapter 2: Virtual LANs and VLAN Trunking  67 

**Key Topic** 

trunk on SW1, however, the tag 100 will be rewritten to 199 and forwarded to SW2, allowing the R1 on the promiscuous trunk to communicate with stations on SW2. 

So, in essence, the special nature of these trunks lies in the tag rewriting they perform: 

- A Promiscuous PVLAN Trunk port rewrites the secondary VLAN ID into the pri mary PVLAN ID upon sending a frame. When a frame is received, no tag manipulation is performed. Also, no tag manipulation is performed for frames in ordinary VLANs. 

- An Isolated PVLAN Trunk port rewrites the primary VLAN ID into the isolated secondary VLAN ID upon sending a frame. When a frame is received, no tag manipulation is performed. Also, no tag manipulation is performed for frames in ordinary VLANs. 

Special Private VLAN Trunk types are supported only on selected higher-level Catalyst switches. 

Example  2-5 shows the configuration of a switch with Private VLANs. Configuration of ordinary trunks is not shown, as there is nothing specific regarding it. 

**Key Topic** 

**Example 2-5** _Configuring Private VLANs_ 

~~! If not running VTPv3, a switch must be put into VTP Transparent mode before~~ 

~~! configuring Private VLANs~~ AccessSw(config)# **vtp mode transparent** Setting device to VTP Transparent mode for VLANS. 

~~! One isolated secondary VLAN and three community secondary VLANs will now be ! created. Afterwards, they will be associated with the primary VLAN 100.~~ 

AccessSw(config)# **vlan 199** AccessSw(config-vlan)# **name Isolated** AccessSw(config-vlan)# **private-vlan isolated** AccessSw(config-vlan)# **vlan 101** AccessSw(config-vlan)# **name Community1** AccessSw(config-vlan)# **private-vlan community** AccessSw(config-vlan)# **vlan 102** AccessSw(config-vlan)# **name Community2** AccessSw(config-vlan)# **private-vlan community** AccessSw(config-vlan)# **vlan 103** AccessSw(config-vlan)# **name Community3** AccessSw(config-vlan)# **private-vlan community** AccessSw(config-vlan)# **vlan 100** AccessSw(config-vlan)# **name Primary1** AccessSw(config-vlan)# **private-vlan primary** AccessSw(config-vlan)# **private-vlan association 101-103,199** AccessSw(config-vlan)# **exit** 

68  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

~~! The~~ ~~**show vlan private-vlan** command is useful to verify the types and associations ! of private VLANs and their member ports. At this moment, there are no ports ! assigned to these VLANs yet.~~ 

AccessSw(config)# **do show vlan private-vlan** 

Primary Secondary Type              Ports ------- --------- ----------------- -----------------------------------------100     101       community 100     102       community 100     103       community 100     199       isolated 

~~! Now, ports will be assigned to these VLANs: ! Fa0/1 - 3:  Secondary community VLAN 101 ! Fa0/4 - 5:  Secondary community VLAN 102 ! Fa0/6 - 8:  Secondary community VLAN 103 ! Fa0/9 - 12: Secondary isolated  VLAN 199 ! Fa0/13:     Promiscuous port in primary VLAN 100 ! For brevity purposes, only the configuration of Fa0/1 - 3 will be shown, as all ! other ports in secondary VLANs, isolated or community, are configured similarly ! Afterwards,~~ ~~**show vlan private-vlan** is issued to verify the port assignment. ! As Fa0/13 is a promiscuous port, it will be shown in all associated secondary ! VLANs~~ 

AccessSw(config)# **interface range fa0/1 - 3** AccessSw(config-if-range)# **switchport mode private-vlan host** AccessSw(config-if-range)# **switchport private-vlan host-association 100 101** AccessSw(config-if-range)# **interface fa0/13** AccessSw(config-if)# **switchport mode private-vlan promiscuous** AccessSw(config-if)# **switchport private-vlan mapping 100 101-103,199** AccessSw(config-if)# **do show vlan private-vlan** 

Primary Secondary Type              Ports ------- --------- ----------------- -----------------------------------------100     101       community         Fa0/1, Fa0/2, Fa0/3, Fa0/13 100     102       community         Fa0/4, Fa0/5, Fa0/13 100     103       community         Fa0/6, Fa0/7, Fa0/8, Fa0/13 100     199       isolated          Fa0/9, Fa0/10, Fa0/11, Fa0/12, Fa0/13 

~~! If a SVI is used as a gateway for devices associated with the primary VLAN 100,~~ 

~~! it must also be configured as promiscuous~~ 

AccessSw(config-if)# **interface Vlan100** AccessSw(config-if)# **private-vlan mapping 101-103,199** AccessSw(config-if)# **ip address 192.168.100.254 255.255.255.0** 

Chapter 2: Virtual LANs and VLAN Trunking  69 

**Key Topic**

## **VLAN Trunking: ISL and 802.1Q** 

VLAN trunking allows switches, routers, and even PCs with the appropriate network interface cards (NIC) and/or software drivers to send traffic for multiple VLANs across a single link. To know to which VLAN a frame belongs, the sending switch, router, or PC adds a header to the original Ethernet frame, with that header having a field in which to place the VLAN ID of the associated VLAN. This section describes the protocol details for the two trunking protocols, followed by the details of how to configure trunking.

## **ISL and 802.1Q Concepts** 

If two devices are to perform trunking, they must agree to use either Inter-Switch Link (ISL) or 802.1Q, because there are several differences between the two, as summarized in Table  2-3 . 

**Table 2-3** _Comparing ISL and 802.1Q_ 

|**Table 2-3** _Comparing ISL and_|_802.1Q_||
|---|---|---|
|**Feature**|**ISL**|**802.1Q**|
|VLANs supported|Normal and extended range1Normal and extended range||
|Protocol defined by|Cisco|IEEE|
|Encapsulates original frame or|Encapsulates|Inserts tag|
|inserts tag|||
|Has a concept of native VLAN|No|Yes|



1 ISL originally supported only normal-range VLANs, but was later improved to support extended-range VLANs as well. 

ISL and 802.1Q differ in how they add a header to the Ethernet frame before sending it over a trunk. ISL adds a new 26-byte header, plus a new trailer (to allow for the new FCS value), encapsulating the entire original frame. This encapsulating header uses the source address (listed as SA in  Figure  2-4 ) of the device doing the trunking, instead of the source MAC of the original frame. ISL uses a multicast destination address (listed as DA in Figure  2-4 ) of either 0100.0C00.0000 or 0300.0C00.0000. Overall, though, an ISL frame is technically a SNAP-encapsulated frame. 

802.1Q inserts a 4-byte header, called a tag, into the original frame (right after the Source Address field). The original frame’s addresses are left intact. Normally, an Ethernet controller would expect to find either an Ethernet Type field or 802.3 Length field right after the Source Address field. With an 802.1Q tag, the first 2 bytes after the Address fields hold a registered Ethernet type value of 0x8100, which implies that the frame includes an 802.1Q header. Because 802.1Q does not actually encapsulate the original frame, it is often called _frame tagging_ .  Figure  2-4 shows the contents of the headers used by both ISL and 802.1Q. 

70  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0111-01.png)


**----- Start of picture text -----**<br>
ISL Header CRC<br>Key  Encapsulated Ethernet Frame<br>Topic 26 bytes 4 bytes<br>DA   Type   User   SA   LEN   AAAA03   HSA   VLAN   BPDU   INDEX   RES<br>VLAN BPDU<br>Dest Src Len/Etype Data FCS Original<br>Frame<br>Dest Src Etype Tag Len/Etype Data FCS Tagged<br>Frame<br>Priority VLAN-ID<br>**----- End of picture text -----**<br>


**Figure 2-4** _ISL and 802.1Q Frame Marking Methods_ 

Finally, the last row from  Table  2-3 refers to the _native VLAN_ . On trunks, 802.1Q does not tag frames sent inside the native VLAN, and assigns all received untagged frames to the native VLAN. The native VLAN feature allows a switch to attempt to use 802.1Q trunking on an interface, but if the other device does not support trunking, the traffic for that one native VLAN can still be sent over the link. By default, the native VLAN is VLAN 1, which is also the default access VLAN. It is absolutely necessary that the native VLANs on both ends of a trunk link match; otherwise a native VLAN mismatch occurs, causing the two VLANs to effectively merge. To detect and possibly avoid any ill effects of a native VLAN mismatch, Cisco switches implement a proprietary extension to PVST+ and Rapid PVST+ that allows them to detect and block the mismatched native VLANs on the trunk. This extension is described in more detail in  Chapter  3 , “Spanning Tree Protocol.” Also, Cisco Discovery Protocol (CDP) will detect and report a native VLAN mismatch. As a best practice, on each trunk, its native VLAN should be changed from VLAN 1 to a different VLAN, and this VLAN should not be used for any other purpose except being configured as a native VLAN. This prevents users from attempting a VLAN hopping attack by sending double-tagged frames that would be detagged on trunks if the top tag matches the trunk’s native VLAN. 

Detailed information about the ISL and 802.1Q tagging as implemented by Cisco can be found at Cisco.com published as a technote document called “Inter-Switch Link and IEEE 802.1Q Frame Format,” Document ID: 17056. 

Chapter 2: Virtual LANs and VLAN Trunking  71

## **ISL and 802.1Q Configuration** 

Cisco switches use the _Dynamic Trunk Protocol (DTP)_ to dynamically learn whether the device on the other end of the cable wants to perform trunking and, if so, which trunking protocol to use. It is meant both to ease the initial deployment of a switched network and to minimize configuration errors that result from mismatched port configuration on an interconnection between two switches. 

DTP learns whether to trunk based on the DTP mode defined for an interface. The individual DTP modes are 

- **dynamic auto:** The port will negotiate the mode automatically; however, it prefers to be an access port. 

- **dynamic desirable:** The port will negotiate the mode automatically; however, it prefers to be a trunk port. 

Out of these modes, **dynamic desirable** has a higher priority—if both ports are dynamic but one is configured as auto and the other as desirable, the resulting operating mode will be trunk. DTP also negotiates the type of encapsulation on the trunk should either of the two devices support both ISL and 802.1Q. If both devices support both trunk types, they will choose ISL. Should the DTP negotiation fail, any port in dynamic mode, either desirable or auto, will be operating as an access port. An upcoming section, “Trunk Configuration Compatibility,” covers the different DTP modes and their combinations in closer detail. 

Different types of Cisco switches have different default DTP modes. For example, earlier Catalyst 2950 and 3550 models default to dynamic desirable mode. Later Catalyst models, such as 2960, 3560 or 3750, default to dynamic auto mode. Authoritative information pertaining to the particular switch platform and IOS version can be found in the appropriate Command Reference. 

While DTP and VTP are independent protocols, DTP carries the VTP domain name in its messages. Switches will successfully negotiate the link operating mode only if the VTP domain name on both switches is the same, or one switch has no VTP domain name configured yet (that is, it uses a NULL domain name). The reason behind tying the DTP negotiation to the VTP domain name is that in different VTP domains, there might be different sets of VLANs, and identically numbered VLANs might be used for different purposes (that is why the network was split into several VTP domains in the first place—to keep the VLAN databases separate and independent). As a result, switches should not try to bring up the link as a trunk, as extending VLANs from one VTP domain to another can have undesired consequences. 

With the DTP mode set to desirable, switches can simply be connected, and they should dynamically form a trunk. You can, however, configure trunking details and verify the results with **show** commands.  Table  2-4 lists some of the key Catalyst IOS commands related to trunking. 

72  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 2-4** _VLAN Trunking–Related Commands_ 

|**Key**<br>**Topic**||
|---|---|
||**Command**<br>**Function**|
||**switchport **|**no switchport**<br>Toggle defining whether to treat the interface as a switch<br>interface (**switchport**) or as a routed interface (**no switchport**)|
||**switchport mode ...**<br>Sets DTP negotiation parameters|
||**switchport trunk ...**<br>Sets trunking parameters if the interface is trunking|
||**switchport access ...**<br>Sets nontrunking-related parameters if the interface is not<br>trunking|
||**show interfaces trunk**<br>Summary of trunk-related information|
||**show interfaces ** _type_<br>_number_ **trunk**<br>Lists trunking details for a particular interface|
||**show interfaces ** _type_<br>_number_ **switchport**<br>Lists both trunking and nontrunking details for a particular<br>interface|



Figure  2-5 lists several details regarding Switch1’s trunking configuration and status, as shown in  Example  2-6 . R1 is not configured to trunk, so Switch1 will fail to negotiate trunking. Switch2 is a Catalyst 3550, which supports both ISL and 802.1Q, so they will negotiate trunking and use ISL. Switch3 and Switch4 are Catalyst 2950s, which support only 802.1Q; as a result, Switch1 negotiates trunking, but picks 802.1Q as the trunking protocol. While both Catalyst 3550 and 2950 are End-of-Life at the time of writing, their default port settings of dynamic desirable serve a useful example of how simply interconnecting them results in links dynamically becoming trunks. With recent Catalyst models, such as 2960, 3560, 3750, or 3850 Series, the default setting is **dynamic auto** , so the same topology in  Figure  2-5 equipped with any of these platforms would negotiate all connected ports to operate in access mode. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0113-04.png)


**----- Start of picture text -----**<br>
Not Configured<br>to Trunk<br>Fa0/1 Gi0/1 Defaults to DTP Desirable<br>R1 SW1 Fa0/24 SW2 Supports ISL or .1Q<br>Fa0/12<br>Defaults to DTP Desirable Defaults to DTP Desirable<br>Does Not Support ISL (2950) SW3 SW4 Does Not Support ISL (2950)<br>**----- End of picture text -----**<br>


**Figure 2-5** _Trunking Configuration Reference for  Example  2-6_ 

Chapter 2: Virtual LANs and VLAN Trunking  73 

**Example 2-6** _Trunking Configuration and_ **show** _Command Example – Switch1_ 

~~! The administrative mode of dynamic desirable (trunking) and negotiate (trunking ! encapsulation) means that Switch1 attempted to negotiate to trunk, but the ! operational mode of static access means that trunking negotiation failed. ! The reference to "operational trunking encapsulation" of native means that ! no tagging occurs. Switch1#~~ ~~**show int fa 0/1 switchport**~~ Name: Fa0/1 Switchport: Enabled Administrative Mode: dynamic desirable Operational Mode: static access Administrative Trunking Encapsulation: negotiate Operational Trunking Encapsulation: native Negotiation of Trunking: On Access Mode VLAN: 1 (default) Trunking Native Mode VLAN: 1 (default) Administrative private-vlan host-association: none Administrative private-vlan mapping: none Operational private-vlan: none Trunking VLANs Enabled: ALL Pruning VLANs Enabled: 2-1001 Protected: false Unknown unicast blocked: disabled Unknown multicast blocked: disabled Voice VLAN: none (Inactive) Appliance trust: none 

~~! Next, the~~ ~~**show int gig 0/1 trunk** command shows the configured mode ! (desirable), and the current status (n-isl), meaning negotiated ISL. Note~~ 

~~! that the trunk supports the extended VLAN range as well.~~ 

~~Switch1#~~ ~~**show int gig 0/1 trunk**~~ 

~~Port      Mode         Encapsulation  Status        Native vlan Gi0/1     desirable    n-isl          trunking      1~~ 

Port      Vlans allowed on trunk Gi0/1     1-4094 

Port      Vlans allowed and active in management domain Gi0/1     1,21-22 

74  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Port      Vlans in spanning tree forwarding state and not pruned Gi0/1     1,21-22 ~~! Next, Switch1 lists all three trunks - the segments connecting to the other ! three switches - along with the type of encapsulation. Switch1#~~ ~~**show int trunk**~~ Port      Mode         Encapsulation  Status        Native vlan Fa0/12    desirable    n-802.1q       trunking      1 Fa0/24    desirable    n-802.1q       trunking      1 Gi0/1     desirable    n-isl          trunking      1 Port      Vlans allowed on trunk Fa0/12    1-4094 Fa0/24    1-4094 Gi0/1     1-4094 Port      Vlans allowed and active in management domain Fa0/12    1,21-22 Fa0/24    1,21-22 Gi0/1     1,21-22 Port      Vlans in spanning tree forwarding state and not pruned Fa0/12    1,21-22 Fa0/24    1,21-22 Gi0/1     1,21-22 

The possibility to configure the port to negotiate its operating mode dynamically also explains why there can be both **switchport access** and **switchport trunk** commands present on a single interface. Though confusing at first sight, these commands merely define how a port would behave _if_ it was operating either as an access or a trunk port. Commands related to a currently unused operating mode of a port might be present but they are ignored. 

As shown in  Example  2-7 , on newer Catalyst platforms, the **show dtp** commands display the operating state of DTP globally and on individual ports. 

**Example 2-7 show dtp** _Command Output on SW1_ 

SW1# **show dtp** Global DTP information Sending DTP Hello packets every 30 seconds Dynamic Trunk timeout is 300 seconds 12 interfaces using DTP 

Chapter 2: Virtual LANs and VLAN Trunking  75 

! The TOS/TAS/TNS stand for Trunk Operating/Administrative/Negotiation Status ! The TOT/TAT/TNT stand for Trunk Operating/Administrative/Negotiation Type ! In the following output, Fa0/12 is configured as dynamic desirable 

SW1# **show dtp interface fa0/12** DTP information for FastEthernet0/12: TOS/TAS/TNS:                              TRUNK/DESIRABLE/TRUNK TOT/TAT/TNT:                              ISL/NEGOTIATE/ISL Neighbor address 1:                       00179446B30E Neighbor address 2:                       000000000000 Hello timer expiration (sec/state):       19/RUNNING Access timer expiration (sec/state):      289/RUNNING Negotiation timer expiration (sec/state): never/STOPPED Multidrop timer expiration (sec/state):   never/STOPPED FSM state:                                S6:TRUNK # times multi & trunk                     0 Enabled:                                  yes In STP:                                   no 

Statistics ---------- 

3 packets received (3 good) 

0 packets dropped 

0 nonegotiate, 0 bad version, 0 domain mismatches, 

0 bad TLVs, 0 bad TAS, 0 bad TAT, 0 bad TOT, 0 other 

6 packets output (6 good) 

3 native, 3 software encap isl, 0 isl hardware native 

0 output errors 

0 trunk timeouts 

2 link ups, last link up on Mon Mar 01 1993, 00:14:09 

2 link downs, last link down on Mon Mar 01 1993, 00:14:02 

**Note** Without any configuration, the default port settings on recent Catalyst switch series such as 2960, 3560, 3750, 3650, and 3850 are as follows: mode set to dynamic auto, native VLAN set to 1, access VLAN set to 1, trunk encapsulation set to auto (if both ISL and dot1q supported) or dot1q, all VLANs allowed, and VLANs 2–1001 eligible for pruning. On older 2950 and 3550 models, the default mode was dynamic desirable. 

76  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## Allowed, Active, and Pruned VLANs 

Although a trunk can support VLANs 1–4094, several mechanisms reduce the actual number of VLANs whose traffic flows over the trunk. First, VLANs can be administratively forbidden from existing over the trunk using the **switchport trunk allowed** interface subcommand. Also, any allowed VLANs must be configured on the switch before they are considered active on the trunk. Finally, VTP can prune VLANs from the trunk, with the switch simply ceasing to forward frames from that VLAN over the trunk. 

The **show interface trunk** command lists the VLANs that fall into each category, as shown in the last command in  Example  2-6 . The categories are summarized as follows:

## **Key Topic** 

- **Allowed VLANs:** Each trunk allows all VLANs by default. However, VLANs can be removed or added to the list of allowed VLANs by using the **switchport trunk allowed** command. 

- **Allowed and active:** To be active, a VLAN must be in the allowed list for the trunk (based on trunk configuration), the VLAN must exist in the VLAN configuration on the switch, and it must be in the active state (not suspended or locally shutdown). With PVST+, an STP instance is actively running on this trunk for the VLANs in this list. 

- **Active and not pruned:** This list is a subset of the “allowed and active” list, with any VTP-pruned VLANs and VLANs for which PVST+ considers the port Blocking removed.

## Trunk Configuration Compatibility 

In most production networks, switch trunks are configured using the same standard throughout the network. For example, rather than allow DTP to negotiate trunking, many engineers configure trunk interfaces to always trunk ( **switchport mode trunk** ) and disable DTP on ports that should not trunk. IOS includes several commands that impact whether a particular segment becomes a trunk. Because many enterprises use a typical standard, it is easy to forget the nuances of how the related commands work. This section covers those small details. 

Two IOS configuration commands impact if and when two switches form a trunk. The **switchport mode** and **switchport nonegotiate** interface subcommands define whether DTP even attempts to negotiate a trunk, and what rules it uses when the attempt is made. Additionally, the settings on the switch ports on either side of the segment dictate whether a trunk forms or not. 

Table  2-5 summarizes the trunk configuration options. The first column suggests the configuration on one switch, with the last column listing the configuration options on the other switch that would result in a working trunk between the two switches. 

Chapter 2: Virtual LANs and VLAN Trunking  77 

**Key Topic** 

**Table 2-5** _Trunking Configuration Options That Lead to a Working Trunk_ 

|**Configuration**|**Short Name**|**Meaning**|**To Trunk,**|
|---|---|---|---|
|**Command on**|||**Other Side**|
|**One Side1**|||**Must Be**|
|**switchport mode**|Trunk|Always trunks on this end; sends|On, desirable,|
|**trunk**||DTP to help other side choose to|auto|
|||trunk||
|**switchport mode**|Nonegotiate|Always trunks on this end; does|On|
|**trunk**;**switchport**||not send nor process DTP messages||
|**nonegotiate**||(good when other switch is a non-||
|||Cisco switch)||
|**switchport mode**|Desirable|Sends DTP messages indicating|On, desirable,|
|**dynamic desirable**||dynamic mode with preferred|auto|
|||trunking, and trunks if negotiation||
|||succeeds||
|**switchport mode**|Auto|Sends DTP messages indicating|On, desirable|
|**dynamic auto**||dynamic mode with preferred access,||
|||and trunks if negotiation succeeds||
|**switchport mode**|Access|Never trunks; can send a single DTP|(Never trunks)|
|**access**||message when entering the access||
|||mode to help other side reach same||
|||conclusion, ceases to send and||
|||process DTP messages afterward||
|**switchport mode**|Access (with|Never trunks; does not send or|(Never trunks)|
|**access**;**switchport**|nonegotiate)|process DTP messages||
|**nonegotiate**||||



1 When the **switchport nonegotiate** command is not listed in the first column, the default (DTP negotiation is active) is assumed. 

**Note** If an interface trunks, the type of trunking (ISL or 802.1Q) is controlled by the setting on the **switchport trunk encapsulation** command if the switch supports multiple trunk encapsulations. This command includes an option for dynamically negotiating the type (using DTP) or configuring one of the two types. 

Also, for DTP negotiation to succeed, both switches must either be configured with the same VTP domain name, or at least one switch must have its VTP domain name unconfigured (that is, NULL).

## **Configuring Trunking on Routers** 

VLAN trunking can be used on routers and hosts as well as on switches. However, routers do not support DTP, so you must manually configure them to support trunking. Additionally, you must manually configure a switch on the other end of the segment to trunk, because the router does not participate in DTP. 

78  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

The majority of router trunking configurations use subinterfaces, with each subinterface being associated with one VLAN. The subinterface number does not have to match the VLAN ID; rather, the **encapsulation** command sits under each subinterface, with the associated VLAN ID being part of the **encapsulation** command. Use subinterface numbers starting with 1; the subinterface number 0 is the physical interface itself (for example, interface Fa0/0.0 is the Fa0/0 itself). Also, because good design calls for one IP subnet per VLAN, if the router wants to forward IP packets between the VLANs, the router needs to have an IP address associated with each trunking subinterface. 

You can configure 802.1Q native VLANs under a subinterface or under the physical interface on a router. If they are configured under a subinterface, you use the **encapsulation dot1q** _vlan-id_ **native** subcommand, with the inclusion of the **native** keyword meaning that frames exiting this subinterface should not be tagged, and incoming untagged frames shall be processed by this subinterface. As with other router trunking configurations, the associated IP address would be configured on that same subinterface. Alternately, if not configured on a subinterface, the router assumes that the native VLAN is associated with the physical interface. In this case, the **encapsulation** command is not needed nor supported under the physical interface; the associated IP address, however, would need to be configured under the physical interface. Configuring an (understandably distinct) IP address on both physical interface and a subinterface under the same physical interface using **encapsulation dot1q** _vlan-id_ **native** , thereby technically resulting in two different interfaces for the native VLAN, is not supported. All incoming untagged frames will be processed by the subinterface configuration only. A notable exception to this rule can be seen on ISR G1 routers equipped with 10-Mbps Ethernet built-in interfaces. On these router platforms, settings for the native VLAN shall be configured on the physical Ethernet interface directly. While the router will accept the configuration of a subinterface with the **encapsulation dot1q** _vlan-id_ **native** command, incoming untagged frames will be processed by the configuration of the physical interface. This exception applies only to ISR platforms with 10-Mbps Ethernet interfaces, and is not present on platforms with Fast Ethernet or faster interfaces. 

If the router supports native VLAN configuration on a subinterface, it is recommended to use subinterfaces instead of putting the native VLAN configuration on a physical port. Aside from keeping the configuration more consistent (all configuration being placed on subinterfaces), this configuration allows the router to correctly process frames that, despite being originated in the native VLAN, carry an 802.1Q tag. Tagging such frames is done when using the CoS field inside an 802.1Q tag. If the native VLAN configuration was done on a physical interface, the router would not be able to recognize that a frame carrying an 802.1Q tag with a nonzero VLAN ID is really a CoS-marked frame in the native VLAN. When using subinterfaces, the **encapsulation dot1q** _vlan-id_ **native** command allows the router to recognize that both untagged frames and CoS-marked frames tagged with the particular _vlan-id_ should be processed as frames in the native VLAN. 

Example  2-8 shows an example configuration for Router1 in  Figure  2-1 , both for ISL and 802.1Q. In this case, Router1 needs to forward packets between the subnets on VLANs 21 and 22. The first part of the example shows ISL configuration, with no native VLANs, and therefore only a subinterface being used for each VLAN. The second part of the example shows an alternative 802.1Q configuration, using the option of placing the native VLAN (VLAN 21) configuration on the physical interface. 

Chapter 2: Virtual LANs and VLAN Trunking  79 

**Key Topic**

## **Example 2-8** _Trunking Configuration on Router1_ 

! Note the subinterface on the Fa0/0 interface, with the **encapsulation** ! command noting the type of trunking, as well as the VLAN number. The subinterface ! number does not have to match the VLAN ID. Also note the IP addresses for ! each interface, allowing Router1 to route between VLANs. ! The **encapsulation** command **must** be entered on a subinterface before entering any ! other IP-related commands, such as configuring an IP address. Router1(config)# **interface fa0/0** Router1(config-if)# **no shutdown** Router1(config-if)# **interface fa0/0.1** Router1(config-subif)# **encapsulation isl 21** Router1(config-subif)# **ip address 10.1.21.1 255.255.255.0** Router1(config-subif)# **interface fa0/0.2** Router1(config-subif)# **encapsulation isl 22** Router1(config-subif)# **ip address 10.1.22.1 255.255.255.0** ~~! Next, an alternative 802.1Q configuration is shown. Note that this configuration ! places the IP address for VLAN 21 on the physical interface; the router simply ! associates the physical interface with the native VLAN. Alternatively, ! a subinterface could be used, with the~~ ~~**encapsulation dot1q 21 native** command ! specifying that the router should treat this VLAN as the native VLAN.~~ Router1(config)# **interface fa0/0** Router1(config-if)# **ip address 10.1.21.1 255.255.255.0** Router1(config-if)# **no shutdown** Router1(config-if)# **interface fa0/0.2** Router1(config-subif)# **encapsulation dot1q 22** Router1(config-subif)# **ip address 10.1.22.1 255.255.255.0** 

Note also that the router does not have an explicitly defined allowed VLAN list on an interface. However, the allowed VLAN list is implied based on the configured VLANs. For example, in this example, when using ISL, Router1 allows VLANs 21 and 22, while when using 802.1Q, it allows the native VLAN and VLAN 22.

## **802.1Q-in-Q Tunneling** 

Traditionally, VLANs have not extended beyond the WAN boundary. VLANs in one campus extend to a WAN edge router, but VLAN protocols are not used on the WAN. 

Today, several emerging alternatives exist for the passage of VLAN traffic across a WAN, including 802.1Q-in-Q, its standardized version 802.1ad called Provider Bridges, another standard 802.1ah called Provider Backbone Bridges, Layer2 Tunneling Protocol (L2TPv3), 

80  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Ethernet over MPLS (EoMPLS), and VLAN Private LAN Services (VPLS). While these topics are more applicable to the CCIE Service Provider certification, you should at least know the concept of 802.1 Q-in-Q tunneling. 

Also known as Q-in-Q on Catalyst switches, 802.1Q-in-Q allows an SP to preserve 802.1Q VLAN tags across a WAN service. By doing so, VLANs actually span multiple geographically dispersed sites.  Figure  2-6 shows the basic idea. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0121-03.png)


**----- Start of picture text -----**<br>
SP:<br>Customer1: VLAN 5<br>Customer2: VLAN 6<br>Eth. VLAN Eth. VLAN<br>Data Data<br>Header ID 100 Header ID 100<br>Eth. VLAN VLAN<br>Data<br>Header ID 5 ID 100<br>C1-SW1 C1-SW2<br>VLANs 100-199<br>SP-SW1 SP-SW2<br>Eth. VLAN VLAN<br>Data<br>C2-SW1 Header ID 6 ID 100 C2-SW2<br>VLANs 100-500<br>Eth. VLAN Eth. VLAN<br>Data Data<br>Header ID 100 Header ID 100<br>**----- End of picture text -----**<br>


**Figure 2-6** _Q-in-Q: Basic Operation_ 

The ingress SP switch takes the 802.1Q frame, and then tags each frame entering the interface with an additional 802.1Q header, called the S-tag (the original customer tags are called C-tags and are not modified nor processed). In this case, all of Customer1’s frames are tagged as VLAN 5 as they pass over the WAN; Customer2’s frames are tagged with VLAN 6. After removing the S-tag at egress, the customer switch sees the original 802.1Q frame with the C-tag intact, and can interpret the VLAN ID correctly. The receiving SP switch (SP-SW2 in this case) can keep the various customers’ traffic separate based on the additional VLAN S-tags. 

Notice that if the trunk between SP-SW1 and SP-SW2 used VLAN 5 as the native VLAN, frames coming from Customer1 would not have an S-tag added on this trunk. As a result, they would be received by SP-SW2 tagged only with the C-tag, and would be processed in the VLAN indicated in the C-tag instead of VLAN 5. This could result in Customer1’s traffic leaking out to another customer, or to be otherwise misforwarded or blackholed. To prevent this, SP’s switches are usually configured with **vlan dot1q tag native** command to essentially deactivate the concept of native VLAN, and to tag all frames on trunks regardless of the native VLAN setting. 

Chapter 2: Virtual LANs and VLAN Trunking  81 

**Key Topic** 

Using Q-in-Q, an SP can offer VLAN services, even when the customers use overlapping VLAN IDs. Customers get more flexibility for network design options, particularly with metro Ethernet services. Plus, CDP and VTP traffic can be configured to pass transparently over the Q-in-Q service. 

On Catalyst switches, the Q-in-Q is supported on 3550 and higher platforms.  Example 2-9 shows the configuration, which is relatively straightforward. 

**Example 2-9** _Q-in-Q Configuration Example on a Catalyst 3560_ 

~~! It is assumed that C1-SW1 and C1-SW2 have their ports towards SP-SW1 configured~~ 

~~! as ordinary 802.1Q trunks. On SP-SW1, the~~ ~~**vlan dot1q tag native** is used to~~ 

~~! force tagging on all VLANs including native VLAN on trunks. Also, because~~ 

~~! a customer's C-tagged frame may already contain 1500 bytes in its payload, this ! payload including the C-tag is considered a new payload in the S-tagged frame,~~ 

~~! and thus may grow up to 1504 bytes. Therefore, the MTU of the resulting frames~~ 

~~! is increased to 1504 bytes using the~~ ~~**system mtu** commands. Their use must also~~ 

~~! be carefully matched by neighboring devices.~~ 

SP-SW1(config)# **vlan dot1q tag native** SP-SW1(config)# **system mtu 1504** ! Applies to 100Mbps interfaces SP-SW1(config)# **system mtu jumbo 1504** ! Applies to 1Gbps and 10Gbps interfaces ! SP-SW1(config)# **vlan 5** SP-SW1(config-vlan)# **name Customer1** SP-SW1(config-vlan)# **exit** SP-SW1(config)# **vlan 6** SP-SW1(config-vlan)# **name Customer2** SP-SW1(config-vlan)# **exit** 

~~! The Fa0/24 interface connects to SP-SW2. This interface is configured as an~~ 

~~! ordinary trunk port~~ 

SP-SW1(config)# **interface FastEthernet0/24** SP-SW1(config-if)# **switchport trunk encapsulation dot1q** SP-SW1(config-if)# **switchport mode trunk** 

~~! The Fa0/1 interface connects to C1-SW1. Here, apart from 802.1Q-in-Q tunneling,~~ 

~~! the switch is also configured to tunnel selected Layer2 management protocols.~~ 

- ~~! To assign all Customer1's traffic to SP's VLAN 5,~~ ~~**switchport access vlan 5** is ! used.~~ 

SP-SW1(config)# **interface FastEthernet0/1** SP-SW1(config-if)# **switchport mode dot1q-tunnel** SP-SW1(config-if)# **switchport access vlan 5** 

82  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

SP-SW1(config-if)# **l2protocol-tunnel cdp** SP-SW1(config-if)# **l2protocol-tunnel lldp** SP-SW1(config-if)# **l2protocol-tunnel stp** SP-SW1(config-if)# **l2protocol-tunnel vtp** 

~~! The Fa0/2 interface connects to C2-SW1. This is the basic 802.1Q-in-Q tunneling~~ 

~~! configuration without any Layer2 management protocol tunneling~~ 

SP-SW1(config)# **interface FastEthernet0/2** SP-SW1(config-if)# **switchport mode dot1q-tunnel** SP-SW1(config-if)# **switchport access vlan 6** 

~~! The show interfaces Fa0/1 switchport shows that the interface is operating~~ 

~~! in QinQ tunneling mode. The~~ ~~**show vlan** (not shown here for brevity) would display ! the Fa0/1 in the Customer1 VLAN just like an ordinary access port.~~ 

SP-SW1# **show interfaces fa0/1 switchport** Name: Fa0/1 Switchport: Enabled Administrative Mode: tunnel Operational Mode: tunnel Administrative Trunking Encapsulation: negotiate Operational Trunking Encapsulation: native Negotiation of Trunking: Off Access Mode VLAN: 5 (Customer1) Trunking Native Mode VLAN: 1 (default) Administrative Native VLAN tagging: enabled Voice VLAN: none Administrative private-vlan host-association: none Administrative private-vlan mapping: none Administrative private-vlan trunk native VLAN: none Administrative private-vlan trunk Native VLAN tagging: enabled Administrative private-vlan trunk encapsulation: dot1q Administrative private-vlan trunk normal VLANs: none Administrative private-vlan trunk associations: none Administrative private-vlan trunk mappings: none Operational private-vlan: none Trunking VLANs Enabled: ALL Pruning VLANs Enabled: 2-1001 Capture Mode Disabled Capture VLANs Allowed: ALL Protected: false Unknown unicast blocked: disabled 

Chapter 2: Virtual LANs and VLAN Trunking  83 

Unknown multicast blocked: disabled Appliance trust: none SP-SW1#

## **VLAN Trunking Protocol** 

VTP advertises VLAN configuration information to neighboring switches so that the VLAN configuration can be made on one switch, with all the other switches in the domain learning the VLAN information dynamically. VTP advertises the VLAN ID, VLAN name, and VLAN type and state for each VLAN. However, VTP does not advertise any information about which ports (interfaces) should be in each VLAN, so the configuration to associate a switch interface with a particular VLAN (using the **switchport access vlan** command) must still be configured on each individual switch. 

The VTP protocol exists in three versions. VTPv1 and VTPv2 are widely supported across the CatOS and IOS-based switching platforms. VTPv3 support on IOS-based switches is, at the time of writing, relatively new. On entry-level Catalyst switches, VTPv3 is supported starting with IOS Release 12.2(52)SE. 

VTPv1 is the default VTP version supported and active on enterprise IOS-based switches. It supports disseminating of normal-range VLANs only. 

VTPv2 enhancements include the following: 

- **Support for Token Ring Concentrator Relay Function and Bridge Relay Function (TrCRF and TrBRF) type VLANs:** These VLANs were used to segment a Token Ring network into multiple logical rings and interconnecting bridges. There is no use for them in Ethernet-based networks. 

- **Support for unknown Type-Length-Value (TLV) records:** VTP messages can contain additional information elements stored as TLV records. A switch running VTPv1 would drop all unrecognized TLVs from received messages, not propagating them farther to neighboring switches. VTPv2-enabled switches keep all TLVs in propagated messages even if they are not recognized. 

- **Optimized VLAN database consistency checking:** In VTPv1, VLAN database consistency checks are performed whenever the VLAN database is modified, either through CLI, SNMP, or VTP. In VTPv2, these consistency checks are skipped if the change was caused by a received VTP message, as the message itself was originated as a result of a CLI or SNMP action that must already have been sanitized. This is really just an implementation optimization. 

There is ongoing confusion regarding the VTP transparent mode. The IOS documentation for earlier Catalyst series appeared to suggest that VTPv1 switches in transparent mode forward VTP messages only if their version and domain match the settings on the transparent switch, while VTPv2 transparent switches allegedly forward VTP messages regardless of their domain and version. Documentation to recent Catalyst switches is less 

84  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

clear, but it states that both VTPv1 and VTPv2 transparent switches check the domain and only forward the message if its domain matches the domain configured on the transparent switch. 

In reality, experiments performed on multiple Catalyst switch types that supported both VTPv1 and VTPv2 show that, regardless of the activated VTP version, a transparent switch whose VTP domain was NULL (that is, unconfigured) forwarded all VTP messages happily. A transparent switch with a configured domain forwarded VTP messages only if their domain matched. 

VTPv3 differs from VTPv2 in the following aspects: 

- **The server role has been modified:** There are two server types in VTPv3: primary and secondary. A primary server is allowed to modify VTP domain contents, and there can be at most one primary server per VTP domain at any time. A secondary server (often called just a server) is not allowed to modify VTP domain contents, but it can be promoted to the role of primary server, retaking the role from the existing primary server if it exists. Ownership of the primary server role is a runtime state that is not stored in the configuration; instead, it is requested in the privileged EXEC mode if necessary. This modification significantly reduces the probability of unintended modification of the VLAN database, as it is not possible to modify the database contents without the concerted effort of making a switch the primary server. 

- **VTPv3 password storage and usage has been improved:** The VTP password can be stored in an encrypted form that cannot be displayed back as plaintext. While this encrypted string can be carried over to a different switch to make it a valid member of the domain, the promotion of a secondary server into the primary server role will require entering the password in its plaintext form. 

- **VTPv3 is capable of distributing information about the full range of VLANs including Private VLANs:** With VTPv3, it is not necessary to use Transparent mode when using extended-range VLANs and Private VLANs. Pruning, however, still applies only to normal-range VLANs, even in VTPv3. 

- **VTPv3 supports the off mode in which the switch does not participate in VTPv3 operations and drops all received VTP messages:** It is also possible to deactivate VTP on a per-trunk basis. 

- **VTPv3 is a generalized mechanism for distributing contents of an arbitrary database, and is not limited to synchronizing VLAN information over a set of switches:** As an example, VTPv3 is also capable of distributing and synchronizing the MST region configuration among all switches in a VTP domain. 

Each Cisco switch uses one of four VTP modes, as outlined in  Table  2-6 . 

Chapter 2: Virtual LANs and VLAN Trunking  85 

**Key Topic** 

**Key Topic** 

**Table 2-6** _VTP Modes and Features_ 

|**Function**|**Server**|**Client**|**Transparent**|**Off**|
|---|---|---|---|---|
||**Mode**|**Mode**|**Mode**|**Mode***|
|Originates VTP advertisements|Yes|Yes|No|No|
|Processes received advertisements to update|Yes|Yes|No|No|
|its VLAN configuration|||||
|Forwards received VTP advertisements|Yes|Yes|Yes|No|
|Saves VLAN configuration in NVRAM or|Yes|Yes|Yes|Yes|
|vlan.dat|||||
|Can create, modify, or delete VLANs using|Yes|No|Yes|Yes|
|configuration commands|||||



* The Off mode is supported only with VTPv3. 

VTPv1 and VTPv2 use four types of messages: 

- **Summary Advertisement:** This message is originated by VTP Server and Client switches every 5 minutes and, in addition, after each modification to the VLAN database. This message carries information about VTP domain name, revision number, identity of the last updater, time stamp of the last update, MD5 sum computed over the contents of the VLAN database and the VTP password (if configured), and the number of Subset Advertisement messages that optionally follow this Summary Advertisement. Summary Advertisement messages do not carry VLAN database contents. 

- **Subset Advertisement:** This message is originated by VTP Server and Client switches after modifying the VLAN database. Subset Advertisements carry full contents of the VLAN database. One Subset Advertisement can hold multiple VLAN database entries. However, multiple Subset Advertisements might be required if the VLAN database is large. 

- **Advertisement Request:** This message is originated by VTP Server and Client switches to request their neighbors send the complete VLAN database or a part of it. Advertisement requests are sent when a VTP Client switch is restarted, when a switch enters the Client mode, or when a Server or Client switch receives a Summary Advertisement with a higher revision number than its own. 

- **Join:** This message is originated by each VTP Server and Client switch periodically every 6 seconds if VTP Pruning is active. Join messages contain a bit field that, for each VLAN in the normal range, indicates whether it is active or unused (that is, pruned). 

At press time, the details about VTPv3 message types were not made public. 

86  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Note** In any VTP version, VTP messages are transmitted and accepted only on trunk ports. Access ports neither send nor accept VTP messages. For two switches to communicate in VTP, they must first be interconnected through a working trunk link.

## **VTP Process and Revision Numbers** 

Let us first have a look at the VTPv1 and VTPv2 update process. Differences in VTPv3 will be explained later. 

In VTPv1 and VTPv2, the update process begins when a switch administrator, from a VTP server switch, adds, deletes, or updates the configuration for a VLAN. When the new configuration occurs, the VTP server increments the old VTP _revision number_ by 1 and advertises the entire VLAN configuration database along with the new revision number. 

The VTP revision number concept allows switches to know when VLAN database changes have occurred. Upon receiving a VTP update, if the revision number in a received VTP update is larger than a switch’s current revision number, it believes that there is a new version of the VLAN database.  Figure  2-7 shows an example in which the old VTP revision number was 3; the server adds a new VLAN (incrementing the revision number to 4), and then propagates the VTP database to the other switches. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0127-06.png)


**----- Start of picture text -----**<br>
1   Add New VLAN<br>Key<br>Topic 2   Rev 3     Rev 4<br>3   Send VTP Advertisement VTP 3   Send VTP Advertisement<br>Server<br>VTP VTP<br>client Client<br>4   Rev 3    Rev 4<br>5   Sync New VLAN Info<br>4   Rev 3         Rev 4<br>5   Sync New VLAN Info<br>**----- End of picture text -----**<br>


**Figure 2-7** _VTP Revision Number Basic Operation_ 

Cisco switches default to use VTP server mode, but they do not start sending VTP updates until the switch has been configured with a VTP domain name. At that point, the server begins to send its VTP updates, with an updated database and revision number each time its VLAN configuration changes. However, the VTP clients in  Figure  2-7 actually do not have to have the VTP domain name configured. If not configured yet, the client will assume that it should use the VTP domain name in the first received VTP update. However, the client does need one small bit of configuration, namely, the VTP mode, as configured with the **vtp mode** global configuration command. As a side note, switches 

Chapter 2: Virtual LANs and VLAN Trunking  87 

must of course be interconnected with trunk links, as VTP messages are exchanged only over trunks. 

VTP clients and servers alike will accept VTP updates from other VTP server and client switches. For better availability, a switched network using VTP needs at least two VTP server switches. Under normal operations, a VLAN change could be made on one server switch, and the other VTP server (plus all the clients) would learn about the changes to the VLAN database. Once learned, both VTP servers and clients store the VLAN configuration in their respective vlan.dat files in flash memory; they do not store the VLAN configuration in NVRAM. 

With multiple VTP servers installed in a LAN, it is possible to accidentally overwrite the VTP configuration in the network. If trunks fail and then changes are made on more than one VTP server, the VTP configuration databases could differ, with different configuration revision numbers. When the formerly separated parts of the LAN reconnect using trunks, the VTP database with a higher revision number is propagated throughout the VTP domain, replacing some switches’ VTP databases. Note also that because VTP clients can actually originate VTP updates, under the right circumstances, a VTP client can update the VTP database on another VTP client or server. In summary, for a newly connected VTP server or client to change another switch’s VTP database, the following must be true: 

- The new link connecting the new switch is trunking. 

- The new switch has the same VTP domain name as the other switches. 

- The new switch’s revision number is higher than that of the existing switches. 

- The new switch must have the same password, if configured on the existing switches. 

To protect a VTP domain from being joined by unauthorized switches, use VTP passwords. VTP Summary Advertisements carry an MD5 hash computed over the VLAN database contents and the VTP password if configured. After receiving an update to the VLAN database in the form of a Summary Advertisement and at least one Subset Advertisement, the receiving switch computes its own MD5 hash over the contents of the VLAN database reconstituted from these messages and its own VTP password, and compares it to the MD5 hash value indicated in the Summary Advertisement. For these MD5 hash values to match, the sending and receiving switch must be using the same VTP password and the messages must be genuine (that is, not changed or tampered with during transit). Contrary to the popular belief, the MD5 hash present in Summary Advertisements is not computed from the VTP password alone. Also, the MD5 hash— being present only in Summary Advertisements—is not used to protect VTP messages themselves. Some installations simply use VTP transparent or off mode on all switches, which prevents switches from ever listening to other switches’ VTP updates and erroneously modifying their VLAN configuration databases.

## 88  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

VTPv3 addresses the problem of inadvertent (or intentional) rewrite of a VLAN database **Key** by introducing the concept of a _primary server_ . A primary server is the only switch **Topic** in a VTPv3 domain whose VLAN database can be propagated throughout the domain. VTPv3 servers and clients will share their VLAN database only if they agree both on the domain name and on the identity of a primary server (given by its base MAC address). Also, a primary server is the only switch that allows an administrator to perform modifications to the VLAN database. 

Other VTPv3 switches configured as servers are called _secondary servers_ . Unlike VTPv1/VTPv2 servers, secondary servers in VTPv3 do not permit an administrator to modify the VLAN database; rather, they are only eligible to be promoted to the role of a primary server, taking over this role from the existing primary server if present. Clients in VTPv3 neither allow an administrator to modify the VLAN database nor are eligible to be promoted to the primary server role. Both secondary servers and clients store a copy of the primary server’s VLAN database and will share it with their neighboring servers and clients that agree on the identity of the primary server. This means that even in VTPv3, a secondary server or a client switch with a higher revision number can overwrite a neighbor’s VLAN database, but for this to occur, these switches must first match on the domain name, primary server’s identity, and VTP password. 

The state of two or more server or client switches in a VTPv3 domain having different **Key** opinions about the identity of a primary server is called a _conflict_ . Conflicting switches **Topic** do not synchronize their VLAN databases even if all other VTP parameters match. This concept of a conflict is at the core of VTPv3’s improved resiliency against inadvertent VLAN database overwrites. Because changes to the VLAN database can only be performed on a primary server, switches that agree on the primary server’s identity also immediately share the primary server’s database. If a switch is disconnected from the network, unless it is the primary server itself, its VLAN database can be modified only if that switch is promoted to a primary server while disconnected. After this switch is connected back to the network, its idea of the primary server’s identity does not match its neighbors’ knowledge about the primary server; that is, a conflict exists. Therefore, even if its revision number is higher, its VLAN database will not be accepted by its neighbors. This way, the possibility of inadvertent VLAN database overwrites is greatly reduced, though not completely avoided. 

There can be at most one primary server in a VTPv3 domain. Only switches configured as VTPv3 servers can be promoted to the role of a primary server, and the promotion is always performed in the privileged EXEC mode by invoking the **vtp primary** command. The state of a primary server is therefore a volatile runtime state that cannot be permanently stored in the configuration. After a primary server is reloaded, it comes back only as a secondary server again. A switch newly promoted to the role of a primary server using the **vtp primary** command will flood its VLAN database to its neighbors, and they will install and flood it further even if the new primary server’s revision number is lower. This way, the new primary server’s database is asserted over the VTP domain. 

With VTPv3, it is no longer possible to reset the configuration revision number to 0 by setting the switch to the transparent mode and back. The revision number will be reset to 0 only by modifying the VTP domain name or by configuring a VTP password. 

Chapter 2: Virtual LANs and VLAN Trunking  89 

If a VTPv3 switch detects an older switch running VTPv1 or VTPv2 on its port, it will revert to VTPv2 operation on that port, forcing the older switch to operate in VTPv2 mode. Cooperation between VTPv3 and VTPv1-only switches is not supported.

## **VTP Configuration** 

VTP sends updates out all active trunk interfaces (ISL or 802.1Q) by default. However, with all default settings from Cisco, switches are in server mode, with no VTP domain name configured, and they do not send any VTP updates. Before any switches can learn VLAN information from another switch, a working trunk must interconnect them, and at least one switch must have a bare-minimum VTP server configuration—specifically, a domain name. 

Example  2-10 shows Switch3 configuring a VTP domain name to become a VTP server and advertise the VLANs it has configured. The example also lists several key VTP **show** commands. (Note that the example begins with VLANs 21 and 22 configured on Switch3, and all default settings for VTP on all four switches. Also keep in mind that the output of various **show** commands can differ from this example depending on your IOS version and VTP version supported/activated.) 

**Example 2-10** _VTP Configuration and_ **show** _Command Example_ 

~~! First, Switch3 is configured with a VTP domain ID of CCIE-domain.~~ Switch3# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. ~~Switch3(config)#~~ ~~**vtp domain CCIE-domain**~~ Changing VTP domain name from NULL to CCIE-domain ~~! Next, on Switch1, the VTP status shows the same revision as Switch3, and it ! learned the VTP domain name CCIE-domain. Note that Switch1 has no VTP-related ! configuration, so it is a VTP server; it learned the VTP domain name from ! Switch3.~~ 

~~Switch1#~~ ~~**show vtp status**~~ VTP Version capable             : 1 to 3 VTP version running             : 1 ~~VTP Domain Name                 : CCIE-domain~~ VTP Pruning Mode                : Disabled VTP Traps Generation            : Disabled Device ID                       : 0023.ea41.ca00 ~~Configuration last modified by 10.1.1.3 at 9-9-13 13:31:46~~ Local updater ID is 10.1.1.1 on interface Vl1 (lowest numbered VLAN interface found) 

90  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Feature VLAN: -------------VTP Operating Mode                : Server Maximum VLANs supported locally   : 1005 Number of existing VLANs          : 7 Configuration Revision            : 2 MD5 digest                        : 0x0E 0x07 0x9D 0x9A 0x27 0x10 0x6C 0x0B 0x0E 0x35 0x98 0x1E 0x2F 0xEE 0x88 0x88 ~~! The~~ ~~**show vlan brief** command lists the VLANs learned from Switch3. Switch1#~~ ~~**show vlan brief**~~ VLAN Name                             Status    Ports ---- -------------------------------- --------- ------------------------------1    default                          active    Fa0/1, Fa0/2, Fa0/3, Fa0/4 Fa0/5, Fa0/6, Fa0/7, Fa0/10 Fa0/11, Fa0/13, Fa0/14, Fa0/15 Fa0/16, Fa0/17, Fa0/18, Fa0/19 Fa0/20, Fa0/21, Fa0/22, Fa0/23 Gi0/2 ~~21   VLAN0021                         active 22   ccie-vlan-22                     active~~ 1002 fddi-default                     act/unsup 1003 token-ring-default               act/unsup 1004 fddinet-default                  act/unsup 1005 trnet-default                    act/unsup 

Example  2-11 shows examples of a few VTP configuration options.  Table  2-7 provides a list of the most used options, along with explanations. 

**Table 2-7** _VTP Global Configuration Options_ 

|**Key**<br>**Topic**||
|---|---|
||**Option**<br>**Meaning**|
||**domain**<br>Sets the name of the VTP domain. Received VTP messages are ignored if the<br>domain name indicated in these messages does not match the receiving switch’s<br>domain name. A switch can be a member of a single domain only.|
||**password **Sets the password to prevent unauthorized switches from joining the domain.<br>The password is taken into account when generating the MD5 hash of the VLAN<br>database. Received VTP updates are ignored if the passwords on the sending<br>and receiving switch do not match. If VTPv3 is used, the password can also<br>be specified as**hidden**, meaning that the password will never be displayed in<br>plaintext in the**show vtp password **output. The**secret **keyword is used when<br>entering the password in an already encrypted form.|



Chapter 2: Virtual LANs and VLAN Trunking  91

## **Option Meaning** 

|**Option**|**Meaning**|
|---|---|
|**mode**|Sets server, client, or transparent mode on the switch. If VTPv3 is supported, it|
||is also possible to set the off mode, effectively disabling VTP on the switch.|
|**version**|Sets VTP version. Configuring the version 1 or 2 on a server switch applies to all|
||switches in the domain. VTPv3 has to be configured manually on each switch.|
||Prior to activating version 3, the switch must use a non-NULL domain name.|
|**pruning**|Enables VTP pruning, which prevents flooding on a per-VLAN basis to switches|
||that do not have any ports configured as members of that VLAN. Regardless of|
||the VTP version, the pruning applies only to normal-range VLANs.|
|**interface**|Specifies the interface whose IP address is used to identify this switch as an|
||updater in VTP updates. By default, a configured IP address from the lowest|
||numbered VLAN SVI interface will be used.|



Example  2-11 shows the use of VTPv3. Differences in running VTPv3 are most visible in the need of designating a selected switch as the primary server using the **vtp primary** command before changes to the VLAN database can be performed on it, and in the way VTP passwords are used. While not shown in the following example, VTPv3 can also be deactivated either globally on the switch using the **vtp mode off** command, or on a perinterface basis using the simple **no vtp** command (the status of VTP on individual interfaces can be conveniently verified using the **show vtp interface** command). It is worth noting that after changing the VTP mode from **off** to any other mode, all existing VLANs except those hardwired into IOS (1, 1002–1005) will be deleted.

## **Example 2-11** _Use of VTPv3 Example_ 

~~! To use VTPv3, each switch has to be configured individually for version 3 opera! tion. It is assumed that all four switches have been converted to VTPv3. Switches ! 1 and 2 are configured as VTP servers, switches 3 and 4 are configured as VTP ! clients. Only the Switch3 configuration is shown here for brevity purposes.~~ Switch3(config)# **vtp version 3** Switch3(config)# Sep  9 15:49:34.493: %SW_VLAN-6-OLD_CONFIG_FILE_READ: Old version 2 VLAN configuration file detected and read OK.  Version 3 files will be written in the future. Switch3(config)# **vtp mode client** Setting device to VTP Client mode for VLANS. 

~~! An attempt to create a new VLAN on Switch1 will fail, as the Switch1 has not yet ! been promoted to the role of primary server. The example also shows how to ! promote it, and subsequently create the VLAN without further obstacles. The "No~~ 

92  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

~~! conflicting VTP3 devices found." statement means that all switches in the VTP ! domain agree on the identity of the current primary server and thus share its ! VLAN database.~~ 

Switch1# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. Switch1(config)# **vlan 23** VTP VLAN configuration not allowed when device is not the primary server for vlan database. Switch1(config)# **do vtp primary** This system is becoming primary server for feature vlan No conflicting VTP3 devices found. Do you want to continue? [confirm] Switch1(config)# 

Sep  9 17:06:59.332: %SW_VLAN-4-VTP_PRIMARY_SERVER_CHG: 0023.ea41.ca00 has become the primary server for the VLAN VTP feature Switch1(config)# **vlan 23** Switch1(config-vlan)# **name ccie-vlan-23** Switch1(config-vlan)# **exit** 

! On Switch3, the show vtp status shows: 

Switch3(config)# **do show vtp status** VTP Version capable             : 1 to 3 VTP version running             : 3 VTP Domain Name                 : CCIE-domain VTP Pruning Mode                : Disabled VTP Traps Generation            : Disabled Device ID                       : 0023.ea93.8e80 Feature VLAN: -------------VTP Operating Mode                : Client Number of existing VLANs          : 8 Number of existing extended VLANs : 0 Maximum VLANs supported locally   : 255 Configuration Revision            : 2 Primary ID                        : 0023.ea41.ca00 Primary Description               : Switch1 MD5 digest                        : 0x2A 0x42 0xC5 0x50 0x4B 0x9C 0xB6 0xDE 0x17 0x8E 0xE0 0xB6 0x2E 0x67 0xA4 0x9C Feature MST: -------------VTP Operating Mode                : Transparent 

Chapter 2: Virtual LANs and VLAN Trunking  93 

Feature UNKNOWN: -------------VTP Operating Mode                : Transparent 

! Trying to promote the Switch3 to the role of primary server would fail, as it is 

! configured to operate as a client: 

Switch3(config)# **do vtp primary** System can become primary server for Vlan feature only when configured as a server 

! The password handling in VTPv3 has been improved. The password can be configured 

! as being hidden, in which case it will never be displayed again in plaintext: 

Switch1(config)# **vtp password S3cr3tP4ssw0rd hidden** Setting device VTP password Switch1(config)# **do show vtp password** VTP Password: 8C70EFBABDD6EC0300A57BE402409C48 

! This string can be used to populate the password setting on other switches 

! without ever knowing the plaintext form, e.g.: 

Switch2(config)# vtp password 8C70EFBABDD6EC0300A57BE402409C48 secret Setting device VTP password 

! After the password is configured in the secret form (or originally configured in 

! the plain form and marked hidden), any attempt to promote a switch to the primary 

! server role will require entering the password in the plaintext form into the 

! CLI. Without knowing the plaintext form of the password, it is not possible to 

! designate a switch as a primary server: 

Switch2(config)# **do vtp primary** 

This system is becoming primary server for feature vlan 

Enter VTP Password: _<entering 8C70EFBABDD6EC0300A57BE402409C48>_ Password mismatch 

Switch2(config)# **do vtp primary** 

This system is becoming primary server for feature vlan 

Enter VTP Password: _<entering S3cr3tP4ssw0rd>_ No conflicting VTP3 devices found. 

Do you want to continue? **[confirm]** Switch2(config)# 

Sep  9 17:10:42.215: %SW_VLAN-4-VTP_PRIMARY_SERVER_CHG: 0017.9446.b300 has become the primary server for the VLAN VTP feature 

94  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## Normal-Range and Extended-Range VLANs 

Because of historical reasons, some VLAN numbers are considered to be _normal_ , whereas some others are considered to be _extended_ . Normal-range VLANs are VLANs 1–1005, and can be advertised through VTP versions 1 and 2. These VLANs can be configured both in VLAN database mode and in global configuration mode, with the details being stored in the vlan.dat file in Flash. 

Extended-range VLANs range from 1006–4094, inclusive. However, if using VTPv1 or VTPv2, these additional VLANs cannot be configured in VLAN database mode, nor stored in the vlan.dat file, nor advertised through VTP. In fact, to configure them, the switch must be in VTP transparent mode. (Also, you should take care to avoid using VLANs 1006–1024 for compatibility with CatOS-based switches.) VTPv3 removes these limitations: Both normal- and extended-range VLANs can be advertised by VTPv3. Also, with VTPv3, information about all VLANs is again stored in the vlan.dat file in Flash. 

Both ISL and 802.1Q support extended-range VLANs today. Originally, ISL began life only supporting normal-range VLANs, using only 10 of the 15 bits reserved in the ISL header to identify the VLAN ID. The later-defined 802.1Q used a 12-bit VLAN ID field, thereby allowing support of the extended range. Following that, Cisco changed ISL to use 12 of its reserved 15 bits in the VLAN ID field, thereby supporting the extended range. 

Table  2-8 summarizes VLAN numbers and provides some additional notes. 

**Table 2-8** _Valid VLAN Numbers, Normal and Extended_ 

||**Table 2-8**|_Valid VLAN_|_Numbers, Normal and_|_Extended_|
|---|---|---|---|---|
|**Key**|||||
|**Topic**|**VLAN**|**Normal or**|**Can Be Advertised**|**Comments**|
||**Number**|**Extended?**|<br>**and Pruned by VTP**||
||||**Versions 1 and 2?**||
||0|Reserved|—|Not available for use|
||1|Normal|No|On Cisco switches, the default VLAN|
|||||for all access ports; cannot be deleted or|
|||||changed|
||2–1001|Normal|Yes|—|
||1002–1005|Normal|No|Defined specifically for use with FDDI|
|||||and TR translational bridging|
||1006–4094|Extended|No|—|
||4095|Reserved|No|Not available for use|

## **Storing VLAN Configuration** 

Catalyst IOS stores VLAN and VTP configuration in one of two places—either in a Flash file called vlan.dat or in the running configuration. (Remember that the term “Catalyst 

Chapter 2: Virtual LANs and VLAN Trunking  95 

**Key Topic** 

IOS” refers to a switch that uses IOS, not the Catalyst OS, which is often called CatOS.) IOS chooses the storage location in part based on the VTP version and mode, and in part based on whether the VLANs are normal-range VLANs or extended-range VLANs.  Table 2-9 describes what happens based on what configuration mode is used to configure the VLANs, the VTP mode, and the VLAN range. (Note that VTPv1/VTPv2 clients also store the VLAN configuration in vlan.dat, and they do not understand extended-range VLANs.) 

**Table 2-9** _VLAN Configuration and Storage for VTPv1 and VTPv2_ 

|**Table 2-9** _VLAN Configuratio_|_n and Storage for VTPv1 and V_|_TPv2_|
|---|---|---|
|**Function**|**When in VTP Server Mode**|**When in VTP**|
|||**Transparent Mode**|
|Normal-range VLANs can be|Both VLAN database and|Both VLAN database and|
|configured from|configuration modes|configuration modes|
|Extended-range VLANs can be|Nowhere—cannot be|Configuration mode only|
|configured from|configured||
|VTP and normal-range VLAN|vlan.dat in Flash|Both vlan.dat in Flash and|
|configuration commands are||running configuration1|
|stored in|||
|Extended-range VLAN|Nowhere—extended range|Running configuration|
|configuration commands are|not allowed in VTP server|only|
|stored in|mode||



1 When a switch reloads, if the VTP mode or domain name in the vlan.dat file and the startup config file differs, the switch uses only the vlan.dat file’s contents for VLAN configuration. 

**Note** The configuration characteristics referenced in Table 2-9 do not include the interface configuration command **switchport access vlan** ; they include the commands that create a VLAN ( **vlan** command) and VTP configuration commands. 

For VTPv3, the situation is greatly simplified: Regardless of the mode (server, client, transparent, or off), both normal- and extended-range VLANs are stored in the vlan.dat file. If transparent or off mode is selected, VLANs are also present in the running-config. 

Of particular interest for those of you stronger with CatOS configuration skills is that when you erase the startup-config file and reload the Cisco IOS switch, you do not actually erase the normal-range VLAN and VTP configuration information. To erase the VLAN and VTP configuration, you must use the **delete flash:vlan.dat** EXEC command. Also note that if multiple switches are in VTP server mode, if you delete vlan.dat on one switch and then reload it, as soon as the switch comes back up and brings up a trunk, it learns the old VLAN database through a VTP update from the other VTP server. 

96  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Configuring PPPoE** 

Although it might seem out of place in this chapter on VLANs and VLAN trunking, Point-to-Point Protocol over Ethernet (PPPoE) fits best here. Somewhat similar to VLANs that virtualize Ethernet switched infrastructure into multiple isolated multiaccess switched environments, PPPoE virtualizes Ethernet into multiple point-to-point sessions between client hosts and an access concentrator, turning the broadcast Ethernet into a point-to-multipoint environment. PPP itself is a great Layer2 protocol for point-to-point links, with capabilities very well suited to a service provider’s needs, such as per-user authentication (and resulting billing), negotiation of allowed higher protocols carried over the PPP link including their settings (such as endpoint IP addresses), negotiation of compression, link bundling (also called multilink), and so on. PPPoE described in RFC 2516 was originally conceived as a method for carrying PPP-based sessions over Ethernet access networks often used in service provider networks, with the PPPoE software client running on a PC equipped with an ordinary Ethernet card. With the advent of Digital Subscriber Line (DSL) technology, the use of PPPoE with DSL allowed for a simple deployment. Client PCs continued to run PPPoE software clients, while a DSL modem connected to a common LAN with the client PCs simply took the Ethernet frames containing PPP datagrams and transmitted them inside a series of ATM cells over the DSL interface, essentially bridging them over the ATM-based DSL network to the Broadband Remote Access Server (BRAS). In the opposite direction, the modem received Ethernet frames encapsulated in series of ATM cells, reconstructed them and forwarded them onto the LAN. As the features of routers improved, the PPPoE client functionality moved from PCs to the router connected to the DSL network itself. 

The PPPoE client feature permits a Cisco IOS router, rather than an endpoint host, to serve as the client in a network. This permits entire LANs to connect to the Internet over a single PPPoE connection terminated at the single router. 

In a DSL environment, PPP interface IP addresses are derived from an upstream DHCP server using IP Configuration Protocol (IPCP), a subprotocol of PPP. Therefore, IP address negotiation must be enabled on the router’s dialer interface. This is done using the **ip address negotiated** command in the dialer interface configuration. 

Because PPPoE introduces an 8-byte overhead (2 bytes for the PPP header and 6 bytes for PPPoE), the MTU for PPPoE is usually decreased to 1492 bytes so that the entire encapsulated frame fits within the 1500-byte Ethernet frame. Additionally, for TCP sessions, the negotiated Maximum Segment Size is clamped down to 1452 bytes, allowing for 40 bytes in TCP and IP headers and 8 bytes in the PPPoE, totaling 1500 bytes that must fit into an ordinary Ethernet frame. A maximum transmission unit (MTU) mismatch can prevent a PPPoE connection from coming up or from properly carrying large datagrams. Checking the MTU setting is a good first step when troubleshooting PPPoE connections. 

Those familiar with ISDN BRI configuration will recognize the dialer interface configuration and related commands in  Example  2-11 . The key difference between ISDN BRI configuration and PPPoE is the **pppoe-client dial-pool-number** command. 

Chapter 2: Virtual LANs and VLAN Trunking  97 

Configuring an Ethernet edge router for PPPoE Client mode is the focus of this section. This task requires configuring the Ethernet interface (physical or subinterface) and a corresponding dialer interface. 

Figure  2-8 shows the topology.  Example  2-12 shows the configuration steps. The first step is to configure the outside Ethernet interface as a PPPoE client and assign it to a dialer interface. The second step is to configure the corresponding dialer interface. Additional steps, including Network Address Translation (NAT) configuration, are also shown. 

DSL CPE Fa0/0 Fa0/1 LAN EdgeRouter Workstations ATM Network DSL Access Access Concentrator Multiplexer **Figure 2-8** _PPPoE Topology for  Example  2-12_ **Example 2-12** _Configuring PPPoE on EdgeRouter_ EdgeRouter# **conf t** EdgeRouter(config)# **interface fa0/0** EdgeRouter(config-if)# **no shutdown** EdgeRouter(config-if)# **ip address 192.168.100.1 255.255.255.0** EdgeRouter(config-if)# **ip nat inside** EdgeRouter(config)# **interface fa0/1** EdgeRouter(config-if)# **no shutdown** EdgeRouter(config-if)# **pppoe-client dial-pool-number 1** EdgeRouter(config-if)# **exit** EdgeRouter(config)# **interface dialer1** EdgeRouter(config-if)# **mtu 1492** EdgeRouter(config-if)# **ip tcp adjust-mss 1452** EdgeRouter(config-if)# **encapsulation ppp** EdgeRouter(config-if)# **ip address negotiated** EdgeRouter(config-if)# **ppp chap hostname Username@ISP** EdgeRouter(config-if)# **ppp chap password Password4ISP** EdgeRouter(config-if)# **ip nat outside** 

**Figure 2-8** _PPPoE Topology for  Example  2-12_ 

**Example 2-12** _Configuring PPPoE on EdgeRouter_ 

98  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

EdgeRouter(config-if)# **dialer pool 1** EdgeRouter(config-if)# **exit** EdgeRouter(config)# **ip nat inside source list 1 interface dialer1 overload** EdgeRouter(config)# **access-list 1 permit 192.168.100.0 0.0.0.255** EdgeRouter(config)# **ip route 0.0.0.0 0.0.0.0 dialer1** 

You can verify PPPoE connectivity using the **show pppoe session** command. Cisco IOS includes debug functionality for PPPoE through the **debug pppoe** [ **data** | **errors** | **events** | **packets** ] command. 

Chapter 2: Virtual LANs and VLAN Trunking  99

## **Foundation Summary** 

This section lists additional details and facts to round out the coverage of the topics in this chapter. Unlike most of the Cisco Press Exam Certification Guides, this “Foundation Summary” does not repeat information presented in the “Foundation Topics” section of the chapter. Please take the time to read and study the details in the “Foundation Topics” section of the chapter as well as review items noted with a Key Topic icon. 

Table  2-10 lists some of the most popular IOS commands related to the topics in this chapter. (The command syntax was retaken from the _Catalyst 3560 Multilayer Switch Command Reference, 15.0(2)SE_ . Note that some switch platforms might have differences in the command syntax.) 

**Table 2-10** _Catalyst IOS Commands Related to  Chapter  2_ 

|**Table 2-10** _Catalyst IOS Commands Relate_|_d to  Chapter  2_|
|---|---|
|**Command**|**Description**|
|**show mac address-table **[**aging-time **||Displays the MAC address table; the security|
|**count **|**dynamic **|**static**] [**address ** _hw-addr_]|option displays information about the|
|[**interface ** _interface-id_] [**vlan ** _vlan-id_]|restricted or static settings|
|**show interfaces **[_interface-id_]**switchport **||Displays detailed information about an|
|**trunk**]|interface operating as an access port or a|
||trunk|
|**show vlan **[**brief **|**id ** _vlan-id_ _|_ **internal usage **||EXEC command that lists information about|
|**name ** _vlan-name_|**private-vlan **|**summary**]|the VLAN|
|**show vtp status**|Lists VTP configuration and status|
||information|
|**switchport mode **{**access **|**dot1q-tunnel **||Configuration command setting nontrunking|
|**dynamic **{**auto **|**desirable**} |**private-vlan**|(**access**,**private-vlan**), tunneling (**dot1q-**|
|{**host | promiscuous**} |**trunk**}|**tunnel**) trunking (**trunk**), and dynamic|
||trunking (**auto **and**desirable**) parameters|
|**switchport nonegotiate**|Interface subcommand that disables DTP|
||messages; interface must not be configured|
||as a dynamic port|
|**switchport trunk **{**allowed vlan ** _vlan-list_}|Interface subcommand used to set|
|| {**encapsulation **{**dot1q **|**isl **|**negotiate**}} ||parameters used when the port is trunking|
|{**native vlan ** _vlan-id_} | {**pruning vlan ** _vlan-list_}||
|**switchport access vlan ** _vlan-id_|Interface subcommand that statically|
||configures the interface as a member of that|
||one VLAN|



100  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Table  2-11 lists the commands related to VLAN creation—both the VLAN database mode configuration commands (reached with the **vlan database** privileged mode command) and the normal configuration mode commands. 

**Note** Some command parameters might not be listed in Table 2-11. 

**Table 2-11** _VLAN Database and Configuration Mode Command List and Comparison_ 

|**VLAN Database**|**Configuration**|
|---|---|
|**vtp **{**domain ** _domain-name_|**password**|**vtp **{**domain ** _domain-name_|**file ** _filename_|
|_password_|**pruning **|**v2-mode **| {**server **|||**interface ** _name_|**mode **{**client **|**server **||
|**client **|**transparent**}}|**transparent | off **} |**password ** _password_[|
||**hidden **|**secret**] |**pruning **|**version ** _number_}|
|**vlan ** _vlan-id_[**name ** _vlan-name_] [**state **{**active**|**vlan ** _vlan-id_|
||**suspend**}]||
|**show **{**current **|**proposed **|**difference**}|No equivalent|
|**apply **|**abort **|**reset**|No equivalent|



**Table 2-12** _Cisco IOS PPPoE Client Commands_ 

|**Command**|**Description**|
|---|---|
|**pppoe-client dial-pool-number**|Configures the outside Ethernet interface on a router|
|_number_|for PPPoE operation and assigns the PPPoE client|
||into a dialer pool to be used later by a dialer interface|
|**debug pppoe **[**data **|**errors **|**events**|Enables debugging for PPPoE troubleshooting|
||**packets**]||



Chapter 2: Virtual LANs and VLAN Trunking  101

## **Memory Builders** 

The CCIE Routing and Switching written exam, like all Cisco CCIE written exams, covers a fairly broad set of topics. This section provides some basic tools to help you exercise your memory about some of the broader topics covered in this chapter.

## **Fill In Key Tables from Memory** 

Appendix  E , “Key Tables for CCIE Study,” on the CD in the back of this book, contains empty sets of some of the key summary tables in each chapter. Print  Appendix  E , refer to this chapter’s tables in it, and fill in the tables from memory. Refer to  Appendix  F , “Solutions for Key Tables for CCIE Study,” on the CD to check your answers.

## **Definitions** 

Next, take a few moments to write down the definitions for the following terms: 

VLAN, broadcast domain, DTP, VTP pruning, 802.1Q, ISL, native VLAN, encapsulation, Private VLAN, promiscuous port, community VLAN, isolated VLAN, promiscuous port, community port, isolated port, 802.1Q-in-Q, Layer 2 protocol tunneling, PPPoE, DSL. 

Refer to the glossary to check your answers.

## **Further Reading** 

The topics in this chapter tend to be covered in slightly more detail in CCNP Switching exam preparation books. For more details on these topics, refer to the Cisco Press CCNP preparation books found at  www.ciscopress.com/ccnp . 

_Cisco LAN Switching_ , by Kennedy Clark and Kevin Hamilton, is an excellent reference for LAN-related topics in general, and certainly very useful for CCIE written and lab exam preparation. 

DTP protocol details are not covered in official Cisco documentation; however, DTP has been filed as U.S. Patent No. 6,445,715, which is publicly available at www.google.com/?tbm=pts . 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0143-00.png)

## **Blueprint topics covered in this chapter:** 

This chapter covers the following subtopics from the Cisco CCIE Routing and Switching written exam blueprint. Refer to the full blueprint in Table I-1 in the Introduction for more details on the topics covered in each chapter and their context within the blueprint. 

- Spanning Tree Protocol 

   - 802.1D STP 

   - 802.1w RSTP 

   - 802.1s MST 

   - Loop Guard 

   - Root Guard 

   - EtherChannel Misconfiguration Guard 

   - BPDU Guard and BPDU Filter 

   - UDLD 

   - Bridge Assurance 

- EtherChannel 

- Troubleshooting Complex Layer 2 Issues

## **CHAPTER 3**

## **Spanning Tree Protocol** 

Spanning Tree Protocol (STP) is probably one of the most widely known protocols covered on the CCIE Routing and Switching written exam. STP has been around for a long time, is used in most every campus network today, and is covered extensively on the CCNP SWITCH exam. This chapter covers a broad range of topics related to STP.

## **“Do I Know This Already?” Quiz** 

Table  3-1 outlines the major headings in this chapter and the corresponding “Do I Know This Already?” quiz questions. 

**Table 3-1** _“Do I Know This Already?” Foundation Topics Section-to-Question Mapping_ 

|**Table 3-1** _“Do I Know This Already?” Foundati_|_on Topics Section-to-Question_|_Mapping_|
|---|---|---|
|**Foundation Topics Section**|**Questions Covered in This**|**Score**|
||**Section**||
|802.1D Spanning Tree Protocol and Improvements|1–8||
|Protecting and Optimizing Spanning Tree|9||
|Configuring and Troubleshooting EtherChannels|10||
|Troubleshooting Complex Layer 2 Issues|11||
|**Total Score**|||



To best use this pre-chapter assessment, remember to score yourself strictly. You can find the answers in  Appendix  A , “Answers to the ‘Do I Know This Already?’ Quizzes.” 

**1.** Assume that a nonroot 802.1D switch has ceased to receive Hello BPDUs. Which STP setting determines how long a nonroot switch waits before trying to choose a new Root Port? 

   - **a.** Hello timer setting on the Root 

   - **b.** MaxAge timer setting on the Root 

   - **c.** ForwardDelay timer setting on the Root 

   - **d.** Hello timer setting on the nonroot switch 

   - **e.** MaxAge timer setting on the nonroot switch 

   - **f.** ForwardDelay timer setting on the nonroot switch 

104  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**2.** Assume that a nonroot 802.1D switch receives a Hello BPDU with the TCN flag set. Which STP setting determines how long the nonroot switch waits before timing out inactive CAM entries? 

   - **a.** Hello timer setting on the Root 

   - **b.** MaxAge timer setting on the Root 

   - **c.** ForwardDelay timer setting on the Root 

   - **d.** Hello timer setting on the nonroot switch 

   - **e.** MaxAge timer setting on the nonroot switch 

   - **f.** ForwardDelay timer setting on the nonroot switch 

**3.** Assume that a nonroot Switch1 (SW1) is Discarding on an 802.1Q trunk connected to Switch2 (SW2). Both switches are in the same MST region. SW1 ceases to receive Hellos from SW2. What timers have an impact on how long Switch1 takes to both become the Designated Port on that link and reach the Forwarding state? 

   - **a.** Hello timer setting on the Root 

   - **b.** MaxAge timer setting on the Root 

   - **c.** ForwardDelay timer on the Root 

   - **d.** Hello timer setting on SW1 

   - **e.** MaxAge timer setting on SW1 

   - **f.** ForwardDelay timer on SW1 

**4.** Which of the following statements are true regarding support of multiple spanning trees over an 802.1Q trunk? 

   - **a.** Only one common spanning tree can be supported. 

   - **b.** Cisco PVST+ supports multiple spanning trees if the switches are Cisco switches. 

   - **c.** 802.1Q supports multiple spanning trees when using IEEE 802.1s MST. 

   - **d.** Two PVST+ domains can pass over a region of non-Cisco switches using 802.1Q trunks by encapsulating non-native VLAN Hellos inside the native VLAN Hellos. 

**5.** When a switch notices a failure, and the failure requires STP convergence, it notifies the Root by sending a TCN BPDU. Which of the following best describes why the notification is needed? 

   - **a.** To speed STP convergence by having the Root converge quickly. 

   - **b.** To allow the Root to keep accurate count of the number of topology changes. 

   - **c.** To trigger the process that causes all switches to use a short timer to help flush the CAM. 

   - **d.** There is no need for TCN today; it is a holdover from DEC’s STP specification. 

Chapter 3: Spanning Tree Protocol  105 

**6.** Two switches have four parallel Ethernet segments, none of which forms into an EtherChannel. Assuming that 802.1D is in use, what is the maximum number of the eight ports (four on each switch) that stabilize into a Forwarding state? 

   - **a.** 1 

   - **b.** 3 

   - **c.** 4 

   - **d.** 5 

   - **e.** 7 

**7.** IEEE 802.1w does not use the exact same port states as does 802.1D. Which of the following are valid 802.1w port states? 

   - **a.** Blocking 

   - **b.** Listening 

   - **c.** Learning 

   - **d.** Forwarding 

   - **e.** Disabled 

   - **f.** Discarding 

**8.** What STP tools or protocols supply a “MaxAge optimization,” allowing a switch to bypass the wait for MaxAge to expire when its Root Port stops receiving Hellos? 

   - **a.** Loop Guard 

   - **b.** UDLD 

   - **c.** BPDU Guard 

   - **d.** Bridge Assurance 

   - **e.** IEEE 802.1w 

**9.** A trunk between switches lost its physical transmit path in one direction only. Which of the following features protect against the STP problems caused by such an event? 

   - **a.** Loop Guard 

   - **b.** UDLD 

   - **c.** Dispute 

   - **d.** PortFast 

106  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**10.** A switch has four Ethernet segments toward its neighbor, with the intention of using them in an EtherChannel. Some settings on the physical ports on this switch might be different and yet these ports will be allowed to be bundled in a single EtherChannel. Which settings do not have to match? 

   - **a.** DTP negotiation settings (auto/desirable/on) 

   - **b.** Allowed VLAN list 

   - **c.** STP per-VLAN port cost on the ports on a single switch 

   - **d.** If 802.1Q, native VLAN 

**11.** A computer’s NIC is hardcoded to 1000 Mbps and full-duplex, and it is connected to a switch whose Fast Ethernet interface is set to autonegotiate speed and duplex. What speed and duplex will the switch use if the autonegotiation on the computer’s NIC is deactivated as a result of hardcoding the speed and duplex? 

   - **a.** 100 Mbps and full-duplex 

   - **b.** 100 Mbps and half-duplex 

   - **c.** 1000 Mbps and full-duplex 

   - **d.** 1000 Mbps and half-duplex 

   - **e.** The link will be inactive. 

Chapter 3: Spanning Tree Protocol  107

## **Foundation Topics**

## **802.1D Spanning Tree Protocol and Improvements** 

Although many CCIE candidates already know STP well, the details are easily forgotten. For example, you can install a campus LAN, possibly turn on a few STP optimizations and security features out of habit, and have a working LAN using STP—without ever really contemplating how STP does what it does. And in a network that makes good use of Layer 3 switching, each STP instance might span only three to four switches, making the STP issues much more manageable—but more forgettable in terms of helping you remember things you need to know for the exam. This chapter reviews the details of IEEE 802.1D STP, and then goes on to related topics—802.1w RSTP, multiple spanning trees, STP optimizations, and STP security features. STP terminology refers to bridges in many places; in the following sections, the words _bridge_ and _switch_ will be used interchangeably with respect to STP. While the upcoming sections about various STP versions might appear lengthy and reiterate on many known facts, be sure to read them very carefully in their entirety. It is always tiresome to read an in-depth discussion about a protocol as notorious as STP—but as we know, it’s details that matter, especially for a CCIE. This chapter tries to put several details about STP straight, cleaning up numerous misconceptions that have crept in the common understanding of STP over the years of its existence. 

Before diving into STP internals, it is worthwhile to comment on a possible naming confusion regarding various STP versions. The first IEEE-standardized STP, also often called the “legacy” STP, was originally described in 802.1D. Its improvements were subsequently published in so-called amendments: The Rapid STP (RSTP) was standardized in amendment 802.1w, while Multiple STP (MSTP) was covered in amendment 802.1s. Since then, the amendments have been integrated into existing standards. The latest 802.1D-2004 standard no longer includes the legacy STP at all (which is considered obsolete), and instead, it covers the RSTP originally found in 802.1w. The 802.1s MSTP is integrated into 802.1Q-2005 and later revisions. With current standards, therefore, RSTP is covered in 802.1D while MSTP is covered in 802.1Q, and legacy STP has been dropped. Still, many people are used to the old naming, with 802.1D referring to STP, 802.1w referring to RSTP, and 802.1s referring to MSTP. 

STP uses messaging between switches to stabilize the network into a logical loop-free topology. To do so, STP causes some interfaces (popularly called _ports_ when discussing STP) to simply not forward or receive traffic—in other words, the ports are in a _Blocking_ state. The remaining ports, in an STP _Forwarding_ state, together provide a loop-free path to every Ethernet segment in the network. 

STP protocol messages are called Bridge Protocol Data Units (BPDU), the basic structure for which is shown in  Figure  3-1 . 

108  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

|Configuration BPDU|Configuration BPDU|Topology Change Notification BPDU|Topology Change Notification BPDU|
|---|---|---|---|
|BPDU Field|Length in Octets|BPDU Field|Length in Octets|
|Protocol Identifier|2|Protocol Identifier|2|
|Protocol Version|1|Protocol Version|1|
|BPDU Type|1|BPDU Type|1|
|Flags|1|||
|Root Bridge ID|8|||
|Root Path Cost|4|||
|Sending Bridge ID|8|||
|Sending Port ID|2|||
|Message Age|2|||
|Max Age|2|||
|Hello Time|2|||
|Forward Delay|2|||

## **Figure 3-1** _Format of STP Bridge Protocol Data Units_ 

For STP, the Protocol Identifier value is set to 0x0000 and the Protocol Version is also set to 0x00. The BPDU Type field identifies two kinds of STP BPDUs: Configuration BPDUs (type 0x00) and Topology Change Notification BPDUs (type 0x80). The Flags field uses 2 bits out of 8 to handle topology change events: the Topology Change Acknowledgment flag and the Topology Change flag. Following the Flags, there is a series of fields identifying the root bridge, distance of the BPDU’s sender from the root bridge, the sender bridge’s own identifier, and the identifier of the port on the sender bridge that forwarded this BPDU. The MessageAge field is an estimation of the BPDU’s age since it was originated by the root bridge. At the root bridge, it is set to 0. Any other switch will increment this value, usually by 1, before forwarding the BPDU further. The remaining lifetime of a BPDU after being received by a switch is MaxAge-MessageAge. Finally, the remaining fields carry the values of STP timers: MaxAge, HelloTime, ForwardDelay. These timer values always reflect the timer settings on the root switch. Timers configured on a nonroot switch are not used and would become effective only if the switch itself became the root switch. 

Bridges and ports are identified by their IDs in BPDUs. Without discussing the exact format at this point, an object in STP that is called “identifier,” or ID, always has a configurable part called the _priority_ , and a fixed part that cannot be modified by management. Both bridges and ports have IDs with configurable priorities. 

STP operation is based on the ability to compare any two arbitrary Configuration BPDUs **Key** and determine which one of them is better, or _superior_ . The other BPDU is called _infe-_ **Topic** _rior_ . To determine which BPDU out of a pair of BPDUs is superior, they are compared in the following sequence of values, looking for the first occurrence of a lower value: 

- Root Bridge ID (RBID) 

- Root Path Cost (RPC) 

Chapter 3: Spanning Tree Protocol  109 

**Key Topic** 

- Sender Bridge ID (SBID) 

- Sender Port ID (SPID) 

- Receiver Port ID (RPID; not included in the BPDU, evaluated locally) 

First, the RBID value in both BPDUs is compared. If one of the BPDUs contains a lower RBID value, this BPDU is declared superior and the comparison process stops. Otherwise, both BPDUs carry the same RBID value and the RPC is compared. Again, if one of the BPDUs carries a lower RPC value, this BPDU is declared superior. In case both BPDUs carry an identical RPC value, the comparison process moves to the SBID. Should the SBID value be also found identical, the SPID will be compared. If even the SPID values in both BPDUs are the same, RPIDs of ports that received the same BPDU are compared. This very last step is very uncommon and would be seen in situations where a single BPDU was received by multiple ports of a single switch, possibly because of multiple connections to a hub or a non-STP switch being placed somewhere in between. In any case, precisely this capability of selecting a single superior BPDU out of a set of BPDUs is at the core of STP’s capability to choose exactly one root bridge per a switched environment, exactly one Root Port on a nonroot bridge, and exactly one Designated Port for each connected network segment, as each of these roles is derived from the concept of a superior BPDU. Only Configuration BPDUs are compared; Topology Change Notification BPDUs do not convey information used to build a loop-free topology and are not compared. Therefore, whenever a comparison of BPDUs is discussed, it is implied that the BPDUs in question are Configuration BPDUs. 

Additionally, an important fact to remember is that each port in STP stores (that is, remembers) the superior BPDU it has either sent or received. As you will see later, Root Ports and Blocking ports store the received BPDU sent by the “upstream” designated switch (because that BPDU is superior to the one that would be sent out from this port), while Designated Ports store their own sent BPDU (because that one is superior to any received BPDU). Essentially, each port stores the Designated Port’s BPDU—whether it is the port itself that is Designated or it is a neighbor’s port. Should a port store a received BPDU, it must be received again within a time interval of MaxAge-MessageAge seconds; otherwise it will expire after this period. This expiry is always driven by the timers in the BPDU, that is, according to timers of the root switch. 

In the following sections, Configuration BPDUs will also be called simply Hello BPDUs or Hellos, as their origination is driven by the Hello timer.

## **Choosing Which Ports Forward: Choosing Root Ports and Designated Ports** 

To determine which ports forward and block, STP follows a three-step process, as listed in Table  3-2 . Following the table, each of the three steps is explained in more detail. 

110  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 3-2** _Three Major 802.1D STP Process Steps_ 

|**Key**<br>**Topic**||
|---|---|
||**Major Step**<br>**Description**|
||Elect the root switch<br>The switch with the lowest bridge ID; the standard bridge ID is<br>2-byte priority followed by a MAC address unique to that switch.|
||Determine each switch’s<br>Root Port<br>The one port on each nonroot switch that receives the superior<br>resulting BPDU from among all received BPDUs on all its ports.|
||Determine the<br>Designated Port for<br>each segment<br>When multiple switches connect to the same segment, this is the<br>switch that forwards the superior BPDU from among all forwarded<br>BPDUs onto that segment.|

## Electing a Root Switch 

Only one switch can be the _root_ of the spanning tree; to select the root, the switches hold an _election_ . Each switch begins its STP logic by creating and sending an STP Hello bridge protocol data unit (BPDU) message, claiming itself to be the root switch. If a switch hears a _superior Hello_ to its own Hello—namely, a Hello with a lower bridge ID—it stops claiming to be root by ceasing to originate and send Hellos. Instead, the switch starts forwarding the superior Hellos received from the superior candidate. Eventually, all switches except the switch with the lowest bridge ID cease to originate Hellos; that one switch wins the election and becomes the root switch. 

The original IEEE 802.1D bridge ID held two fields: 

- The 2-byte Priority field, which was designed to be configured on the various switches to affect the results of the STP election process. 

- A 6-byte MAC Address field, which was included as a tiebreaker, because each switch’s bridge ID includes a MAC address value that should be unique to each switch. As a result, some switch must win the root election. 

The format of the original 802.1D bridge ID has been redefined in amendment 802.1t and since then integrated into 802.1D-2004.  Figure  3-2 shows the original and new format of the bridge IDs. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0151-09.png)


**----- Start of picture text -----**<br>
2 Bytes 6 Bytes<br>Key<br>Topic Priority System ID Original Format<br>(0 – 65,535) (MAC Address) Bridge ID<br>System ID<br>Priority<br>System ID Extension System ID Extension<br>Multiple<br>(Typically Holds VLAN ID) (MAC Address) (MAC Address<br>of 4096<br>Reduction)<br>4 Bits 12 Bits 6 Bytes<br>**----- End of picture text -----**<br>


**Figure 3-2** _IEEE 802.1D STP Bridge ID Formats_ 

Chapter 3: Spanning Tree Protocol  111 

The format was changed mainly because of the advent of multiple spanning trees as supported by Per VLAN Spanning Tree Plus (PVST+) and IEEE 802.1s Multiple Spanning Trees (MST). With the old-style bridge ID format, a switch’s bridge ID for each STP instance (possibly one per VLAN) was identical if the switch used a single MAC address when building the bridge ID. Because VLANs cause a single physical switch to behave as multiple logical switches, having multiple STP instances with the same bridge ID was in violation of the 802.1D that required a distinct bridge ID for each switch. Vendors such as Cisco used a different MAC address for each VLAN when creating the old-style bridge IDs. This provided a different bridge ID per VLAN, but it consumed a large number of reserved MAC addresses in each switch. 

The System ID Extension, originally described in IEEE 802.1t, allows a network to use multiple instances of STP, even one per VLAN, but without the need to consume a separate MAC address on each switch for each STP instance. The System ID Extension field allows the VLAN ID to be placed into what was formerly the last 12 bits of the Priority field. A switch can use a single MAC address to build bridge IDs and, with the VLAN number in the System ID Extension field, still have a unique bridge ID in each VLAN. The use of the System ID Extension field is also called _MAC address reduction_ , because of the need for many fewer reserved MAC addresses on each switch. The use of the System ID Extension on a switch is indicated by the presence of the **spanningtree extend system-id** command in global configuration mode. Older switches equipped with a larger reserve of MAC addresses allow this command to be removed, reverting to the old-style bridge IDs. Recent switches, however, do not allow this command to be removed even though it is displayed in the running config, and always use the System ID Extension.

## Determining the Root Port 

After the root switch is elected, the rest of the switches now need to determine their _Root Port (RP)_ . The process proceeds as described in the following list: 

**Key Topic** 

**1.** The root switch creates and sends a Hello every Hello timer (2 seconds by default). This Hello contains the RBID and SBID fields set to the ID of the root, RPC set to 0, and SPID set to the identifier of the egress port. 

**2.** Each nonroot switch receiving a BPDU on a particular port adds that port’s cost to the RPC value in the received BPDU, yielding a _resulting_ BPDU. Subsequently, the switch declares the port receiving the superior resulting BPDU as its Root Port. 

**3.** Hellos received on the Root Port of a nonroot switch are forwarded through its remaining designated ports after updating the RPC, SBID, SPID, and MessageAge fields accordingly. Hellos received on other ports of a nonroot switch are processed but they are not forwarded. 

**4.** Switches do not forward Hellos out Root Ports and ports that stabilize into a Blocking state. Hellos forwarded out these ports would be inferior (and therefore uninteresting) to Hellos originated by some neighboring switch’s Designated Port on those segments. 

112  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

The result of this process is that each nonroot switch chooses exactly one port as its Root Port, as there is always only a single received Hello that is superior over all other received Hellos. According to the sequence of compared fields in received Hellos when selecting a superior BPDU, a Root Port always provides the least-cost path toward the switch with the lowest Bridge ID (that is, the root switch). If there are multiple equal-cost paths, additional tiebreakers (SBID, SPID, RPID) will allow the receiving switch to always choose exactly one path in a deterministic fashion: first, port toward the neighbor with the lowest Bridge ID; then, if there are multiple links toward that neighbor, port connected to the neighbor’s port with the lowest Port ID; and finally, if the same BPDU is received on multiple ports at once, the receiving port with the lowest Port ID. 

In this sense, the STP operation is quite similar to the operation of the Routing Information Protocol (RIP), the simplest distance-vector routing protocol. Just like RIP, STP tries to find the least-cost path toward a particular destination, in this case, the root bridge, and has additional criteria to select a single path if there are multiple least-cost paths available. Hellos can be likened to RIP Update messages with RBID identifying the _destination_ , RPC expressing the next hop’s _metric_ to the destination, SBID being the _next-hop identifier_ , and SPID identifying the _next hop’s interface_ . Each time a Hello is received, the receiving switch can be thought to reevaluate its choice of a Root Port and updates the choice if necessary, just like a RIP router receives updates every 30 seconds and reevaluates its choice of least-cost paths to individual destinations. In fact, STP can be seen as a special case of a timer-driven distance-vector routing protocol, selecting exactly one path to exactly one particular destination, the root bridge. This makes STP similar to, though of course not entirely analogous to, RIP. 

A switch must examine the RPC value in each Hello, plus the switch’s STP port costs, to determine its least-cost path to reach the root. To do so, the switch adds the cost listed in the Hello message to the switch’s port cost of the port on which the Hello was received. For example,  Figure  3-3 shows the loop network design and details several STP cost calculations. 

Loop Design – All Port Costs 19 Unless Shown 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0153-05.png)


**----- Start of picture text -----**<br>
Root Hello Cost 0 Adding my incoming cost<br>setting fields for forwarder’s<br>Cost 19 bridge ID, port priority, and<br>SW1 DP RP SW2 port number.<br>DP Cost 1 DP<br>Hello Cost 0 Hello Cost 19<br>Cost out fa0/1 = 0 +<br>100 = 100; cost out<br>fa0/4 = 38 + 19 = 57!<br>Fa0/1<br>Cost 100 BL RP Cost 19<br>RP DP<br>SW3 Fa0/4 SW4<br>Cost 19<br>Hello Cost 38<br>**----- End of picture text -----**<br>


**Figure 3-3** _Calculating STP Costs to Determine RPs_ 

Chapter 3: Spanning Tree Protocol  113 

In  Figure  3-3 , SW1 happened to become root, and is originating Hellos of cost 0. SW3 receives two Hellos, one with cost 0 and one with cost 38. However, SW3 must then calculate its cost to reach the root, which is the advertised cost (0 and 38, respectively) plus SW3’s port costs (100 and 19, respectively). As a result, although SW3 has a direct link to SW1, the calculated cost is lower out interface Fa0/4 (cost 57) than it is out interface Fa0/1 (cost 100), so SW3 chooses its Fa0/4 interface as its RP. 

**Note** Many people think of STP costs as being associated with a segment; however, the cost is actually associated with interfaces. Good design practices dictate using the same STP cost on each end of a point-to-point Ethernet segment, but the values can be different. 

While the costs shown in  Figure  3-3 might seem a bit contrived, the same result would **Key** happen with default port costs if the link from SW1 to SW3 were Fast Ethernet (default **Topic** cost 19), and the other links were Gigabit Ethernet (default cost 4).  Table  3-3 lists the default port costs according to various revisions of the IEEE 802.1D standard. Before 802.1D-1998, IEEE did not specify any recommended STP port cost values for different link speeds in their standard. Speeds shown in  Table  3-3 were chosen by Cisco and used in its STP implementations of that time. The 802.1D-1998 revision of the standard provided a table of recommended values, but as the speeds of Ethernet links continued to increase dramatically, IEEE revised these recommended values again in its 802.1D-2004 revision of the standard. On recent Catalyst switches, the default costs correspond to the 802.1D-1998 version of the standard if PVST or Rapid PVST is used, and to the 802.1D2004 version if MSTP is used. With PVST and Rapid PVST, the 802.1D-2004 costs can be activated using the **spanning-tree pathcost method long** global configuration command. By default, **spanning-tree pathcost method short** is configured, causing the switch to use the older revision of the costs. 

**Table 3-3** _Default Port Costs_ 

|**Table 3-3** _De_|_fault Port Costs_|||
|---|---|---|---|
|**Port speed**|**Pre-802.1D-1998**|**802.1D-1998**|**802.1D-2004**|
||**Cost**|**Cost**|**Cost**|
|10 Mbps|100|100|2000000|
|100 Mbps|10|19|200000|
|1 Gbps|1|4|20000|
|10 Gbps|1|2|2000|

## Determining the Designated Port 

A converged STP topology results in only one switch forwarding Hellos onto each LAN segment. The switch that forwards Hellos onto a LAN segment is called the _designated switch_ for that segment, and the port that it uses to forward frames onto that segment is 

114  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

called the _Designated Port (DP)_ . All remaining ports on a switch that have been determined as neither Root nor Designated will be moved to Blocking state. In the following text, they will be labeled as Non-Designated ports.

## **Key Topic** 

To win the right to be the DP, a switch must send superior Hellos onto the segment. For example, consider the segment between SW3 and SW4 in  Figure  3-3 before the DP has been determined on that segment. SW3 would get Hellos directly from SW1, compute its cost to the root over that path, and then forward the Hello out its Fa0/4 interface to SW4, with RPC set to 100. Similarly, SW4 will forward a Hello with RPC of 38, as shown in  Figure  3-3 . SW4’s port on this segment becomes the DP, as it sends superior Hellos because of their lower RPC value. Even after SW3 selects its Fa0/4 as the Root Port (as it receives superior resulting BPDUs from among all ports on SW3), any Hellos sent from SW3’s Fa0/4 port would indicate the RPC of 57, still being inferior to SW4’s Hellos. 

Only the DP forwards Hellos onto a LAN segment. In the same example, SW4 keeps sending the Hellos with an RPC of 38 out the port, but SW3 stops sending its inferior Hellos. There would be no harm if SW3 continued to send its inferior BPDUs out its Fa0/1 and Fa0/4 ports, but because STP always cares only for superior BPDUs, this would be a waste of effort. Therefore, neither Root Ports nor ports in the Blocking state send BPDUs. 

The tiebreakers during DP selection are the same as before: first, the switch with the least-cost path to the root identified by the lowest Bridge ID; then the neighboring switch with the lowest Bridge ID; and finally the port on the neighbor with the lowest Bridge ID with the lowest Port ID. 

To sum up the rules:

## **Key Topic** 

- The root switch is the switch that has the lowest Bridge ID in the topology. 

- On each nonroot switch, a Root Port is the port receiving the best (that is, superior) resulting BPDUs from all received BPDUs on all ports. The adjective “resulting” refers to the addition of the port’s cost to the BPDU’s RPC value before comparing the received BPDUs. 

- On each connected segment, a Designated Port is the port sending the best (that is, superior) BPDUs on the segment. No modifications to the BPDUs are performed; BPDUs are compared immediately. 

- All ports that are neither Root Ports nor Designated Ports are superfluous in an active topology and will be put into the Blocking state. 

- Configuration BPDUs are sent out only from Designated Ports. Root and NonDesignated ports do not emit Configuration BPDUs because they would be inferior to BPDUs of a Designated Port on this segment and hence ignored. 

Chapter 3: Spanning Tree Protocol  115 

- Each port stores the best (that is, superior) BPDU it has received or sent itself. Designated Ports store the BPDU they send; Root and Blocking ports store the best BPDU they receive. The stored BPDU determines the role of the port and is used for comparisons. 

- Received superior stored BPDUs will expire in MaxAge-MessageAge seconds if not received within this time period.

## **Converging to a New STP Topology** 

Although STP is very illustratively described in the three steps discussed earlier, this approach also gives an impression that after the three steps are completed, STP effectively goes dormant until a topology change occurs. Such impression would be incorrect, though. In reality, STP never stops working. With each received BPDU, a switch reevaluates its own choice of the root switch, Root Port, and Designated/Non-Designated Ports, effectively performing all three steps all over again. In a stable topology, received BPDUs do not change, and therefore, processing them yields the same results again and again. This is similar to the operation of the RIP that also never stops running—it’s just that in a stable network which has converged, processing periodic received updates produces the same set of best paths, which gives off an impression that the protocol has done its job and has stopped. In reality, both STP and RIP continue running indefinitely, only in a stable and converged topology, each run produces the same results. 

Of course, a topology in which STP runs can change over time, and STP has to react appropriately. In precise terms, for STP, a _topology change_ is an event that occurs when 

**Key Topic** 

- A Topology Change Notification BPDU is received by a Designated Port of a switch 

- A port moves to the Forwarding state and the switch has at least one Designated Port (meaning that it is not a standalone switch with just a Root Port connected to an upstream switch and no other connected ports) 

- A port moves from Learning or Forwarding to Blocking 

- A switch becomes the root switch 

When a change to the topology occurs, the elementary reaction of switches that detect the topology change is to start originating BPDUs with appropriately updated contents, propagating the information to their neighbors. These neighbors will process the updated BPDUs, reevaluating their choice of the root switch, Root Port, and Designated/NonDesignated Ports with each received BPDU as usual, and forwarding the BPDU farther according to usual STP rules. 

For an example, consider  Figure  3-4 , which shows the same loop network as in  Figure 3-3 . In this case, however, the link from SW1 to SW2 has just failed. 

116  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Loop Design – All Port Costs 19 Unless Shown 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0157-02.png)


**----- Start of picture text -----**<br>
MAC 0200.1111.1111 1<br>Root My RP failed. I am<br>receiving no other Hellos.<br>I must be the root now!<br>SW1 Disabled Disabled SW2<br>R1<br>Cost 1 Fa0/4<br>1 Hello Root = Hello  Root = 2<br>Sw1 Cost 0 Sw2  Cost 0<br>SW1’s bridge ID is better.<br>So I’m sending the<br>superior Hello on this<br>Fa0/1 segment.  I am now DP! Fa0/2<br>Cost 100<br>Fa0/3<br>SW3 Fa0/4 SW4<br>Cost 19<br>4 Sw1  Hello Cost 100 Root = Sw2  Hello Cost 19 Root = 3<br>**----- End of picture text -----**<br>


**Figure 3-4** _Reacting to the Loss of Link Between SW1 and SW2_ 

The following list describes some of the key steps from  Figure  3-4 : 

**1.** SW2’s Root Port goes down. On SW2, the loss of a Root Port causes it to reelect its Root Port by choosing the port receiving superior resulting BPDUs. However, as the only remaining port is Fa0/4 connected to SW4, and SW4 did not send any BPDUs to SW2 from its Root Port Fa0/2, SW2 has no received BPDUs to choose from, and it will start considering itself a root switch, flooding its own Hellos through all its connected ports. 

**2.** SW4 notices that the latest Hellos indicate a new root switch. However, these Hellos from SW2 received on SW4’s Fa0/2 port, its current Root Port, are inferior to the BPDU stored on that port. When the link between SW1 and SW2 still worked, BPDUs arriving at SW4’s Fa0/4 contained the SW1’s Bridge ID as the RBID. After the link between SW1 and SW2 went down and SW2 started considering itself as the root bridge, its BPDUs arriving at SW4’s Fa0/2 port contained SW2’s Bridge ID as the RBID. However, SW2 has a higher Bridge ID than SW1; otherwise, it would be the root switch right away. Therefore, BPDUs claiming that SW2 is the root bridge are inferior to the BPDU stored on SW4’s Fa0/2 that claims SW1 is the root bridge, and as a result, they are ignored until the BPDU stored on SW4’s Fa0/2 expires. This expiry will take MaxAge-MessageAge, or 20−1=19 seconds. Until then, SW4 does not forward any BPDUs to SW3. 

**3.** During the time SW4 receives inferior BPDUs from SW2 on its Fa0/2 port, it does not forward any BPDUs to SW3. As a result, SW3 ceases to receive BPDUs on its Fa0/4 port, which is its current Root Port. The BPDU stored on SW3’s Fa0/4 port expires in MaxAge-MessageAge, or 20–2=18 seconds. After it expires, Fa0/4 becomes a Designated Port and moves to the Listening state. SW3 then searches for a new Root Port by looking for the superior received resulting BPDU, ultimately choosing Fa0/1 as its new port. Afterward, it will forward SW1’s Hello out its Fa0/4 port after updating the necessary fields. 

Chapter 3: Spanning Tree Protocol  117 

**4.** In the meantime, SW4 might have the BPDU expired from its Fa0/2, started accepting BPDUs from SW2, declared the Fa0/2 as its Root Port toward SW2, and started relaying the Hellos from SW2 to SW3. Even if that was the case, SW3 would treat these Hellos from SW4 as inferior because Hellos sent out from SW3’s Fa0/4 claim that the root switch is SW1 having a lower Bridge ID than SW2. After SW4 receives the relayed Hello from SW3, it will learn about a better root switch than SW2, namely, SW1, and will choose its Fa0/3 as the Root Port. Afterward, it will forward the Hello out its Fa0/2 port. 

**5.** After SW2 receives the forwarded Hello from SW4, it will also learn about SW1 being a better root switch than itself. Therefore, SW2 will stop considering itself as a root switch and will instead declare its Fa0/4 port as the Root Port, finally converging on the new loop-free topology.

## Topology Change Notification and Updating the CAM 

Simply updating the active topology by processing new BPDUs is not sufficient. When STP reconverges on a new active topology, some Content Addressable Memory (CAM) entries might be invalid (CAM is the Cisco term for what is more generically called the MAC address table, switching table, or bridging table on a switch). For example, before the link failure shown in  Figure  3-4 , SW3’s CAM might have had an entry for 0200.1111.1111 (Router1’s MAC address) pointing out Fa0/4 to SW4. Remember, at the beginning of the scenario described in  Figure  3-4 , SW3 was Blocking on its Fa0/1 interface back to SW1. When the link between SW1 and SW2 failed, SW3 would need to change its CAM entry for 0200.1111.111 to point out port Fa0/1. 

STP is not a protocol that tries to find shortest paths toward individual MAC addresses, so it cannot be expected to fill the CAM tables with new correct entries. All STP can do is to instruct switches to age out unused entries prematurely, assuming that the unused entries are exactly those that need updating. Even if good entries are flushed from CAM tables, this does not impair basic connectivity—switches will flood frames to unknown destinations rather than dropping them. 

To update the CAMs, two things need to occur: 

- All switches need to be notified to time out their apparently unused CAM entries. 

- Each switch needs to use a short timer, equivalent to the Forward Delay timer (default 15 seconds), to time out the CAM entries. 

A topology change can start as a highly localized event—a port becoming Forwarding or transitioning from Learning or Forwarding to Blocking on a particular single switch. The information about this change must nevertheless be propagated to all switches in the topology. Therefore, a switch that detects a topology change must notify the root switch, and the root switch in turn can notify all switches in the topology. (Recall that it is the root switch’s Hello that is propagated throughout the network to all switches; a nonroot switch has no way of sending its own Configuration BPDU to all remaining switches in a topology because that BPDU would be inferior, and thus ignored, by possibly many switches.) To do so, a switch detecting a topology change notifies the root switch using 

118  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

a _Topology Change Notification (TCN)_ BPDU. The TCN goes up the tree to the root. After that, the root notifies all the rest of the switches. The process is illustrated in  Figure 3-5 and runs as follows: 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0159-02.png)


**----- Start of picture text -----**<br>
6<br>TCN<br>RB<br>BPDU<br>4<br>TCA 5<br>Conf.<br>BPDU<br>2<br>TCN<br>BPDU<br>TCA<br>3 Conf.<br>BPDU<br>1<br>TC<br>**----- End of picture text -----**<br>


**Figure 3-5** _Propagating Information About Topology Change_ 

   **1.** A topology change event occurs on a port of a switch. 

- **Key Topic 2.** After detecting the event, the switch sends a TCN BPDU out its Root Port; it repeats this message every Hello time until it is acknowledged. 

   **3.** The next designated switch receiving that TCN BPDU sends back an acknowledgment through its next forwarded Hello BPDU by marking the Topology Change Acknowledgment (TCA) bit in the Flags field of the Hello. 

   **4.** The designated switch on the segment in the second step repeats the first two steps, sending a TCN BPDU out its Root Port, and awaits acknowledgment from the designated switch on that segment. 

   **5.** After the TCN arrives at the root switch, it also acknowledges its arrival through sending a BPDU with the Topology Change Acknowledgment bit set through the port through which the TCN BPDU came in. At this point, the root switch has been informed about a topology change that occurred somewhere in the network. 

   **6.** For the next MaxAge+ForwardDelay seconds, the root switch will originate BPDUs with the Topology Change (TC) bit set, instructing all switches to shorten the aging time for CAM entries to ForwardDelay seconds. 

Chapter 3: Spanning Tree Protocol  119 

**Key Topic** 

By each successive switch repeating Steps 2 and 3, eventually the root receives a TCN BPDU. After it is received, the root sets the _Topology Change (TC)_ flag on the next several Hellos (during the next MaxAge+ForwardDelay seconds), which are forwarded to all switches in the network, notifying them that a change has occurred. A switch receiving a Hello BPDU with the TC flag set uses the short (ForwardDelay time derived from the value in the received BPDU, set by the root switch) timer to time out unused entries in the CAM.

## Transitioning from Blocking to Forwarding 

When STP reconverges to a new, stable topology, some ports that were Blocking might have been designated as DP or RP, so these ports need to be in a Forwarding state. However, the transition from Blocking to Forwarding state cannot be made immediately without the risk of causing loops. 

To transition to Forwarding state but also prevent temporary loops, a switch first puts a formerly Blocking port into _Listening_ state, and then into _Learning_ state, with each state lasting for the length of time defined by the ForwardDelay timer (by default, 15 seconds). Table  3-4 summarizes the key points about all the 802.1D STP port states. 

**Table 3-4** _IEEE 802.1D Spanning Tree Interface States_ 

|**Table 3-4** _IEE_|_E 802.1D Spanning T_|_ree Interface States_||
|---|---|---|---|
|**State**|**Forwards Data**|**Learns Source MACs**|**Transitory or Stable**|
||**Frames?**|**of Received Frames?**|**State?**|
|Blocking|No|No|Stable|
|Listening|No|No|Transitory|
|Learning|No|Yes|Transitory|
|Forwarding|Yes|Yes|Stable|
|Disabled|No|No|Stable|



In summary, when STP logic senses a change in the topology, it converges, possibly picking different ports as RP, DP, or neither. Any switch changing its RPs or DPs sends a TCN BPDU to the root at this point. For the ports newly designated as RP or DP, 802.1D STP first uses the Listening and Learning states before reaching the Forwarding state. (The transition from Forwarding to Blocking can be made immediately.)

## **Per-VLAN Spanning Tree and STP over Trunks** 

If only one instance of STP was used for a switched network with redundant links but with multiple VLANs, several ports would be in a Blocking state, unused under stable conditions. The redundant links would essentially be used for backup purposes. 

120  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

The Cisco Per VLAN Spanning Tree Plus (PVST+) feature creates an STP instance for each VLAN. By tuning STP configuration per VLAN, each STP instance can use a different root switch and have different interfaces block. As a result, the traffic load can be balanced across the available links. For example, in the common building design with distribution and access links in  Figure  3-6 , focus on the left side of the figure. In this case, the access layer switches block on different ports on VLANs 1 and 2, with different root switches. Support for PVST+ implies the capability of trunk ports to be selectively blocked or forwarding for individual VLANs. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0161-02.png)


**----- Start of picture text -----**<br>
3560 ISL 3560<br>Root Root<br>VLAN1 VLAN2<br>.1Q .1Q<br>.1Q .1Q<br>FWD FWD<br>VLAN1 VLAN2<br>FWD FWD<br>VLAN2 VLAN1<br>2960 2960<br>**----- End of picture text -----**<br>


**Figure 3-6** _Operation of PVST+ for Better Load Balancing_ 

With different root switches and with default port costs, the access layer switches end up sending VLAN1 traffic over one uplink and VLAN2 traffic over another uplink. 

Using 802.1Q VLANs with IEEE 802.1D STP requires some extra thought as to how it works. Non-Cisco switches that follow exclusively the IEEE standard support only a socalled _Common Spanning Tree (CST)_ . Here, only one instance of STP runs in the network (not even being tied to a specific VLAN because basic STP does not know anything about VLANs), and that one STP topology is used for all VLANs, hence being called as “common.” Although using only one STP instance reduces the STP messaging overhead, it does not allow load balancing by using multiple STP instances, as was shown with PVST+ in  Figure  3-6 . 

When building networks using a mix of Cisco and non-Cisco switches, along with 802.1Q **Key** trunking, you can still take advantage of multiple STP instances in the Cisco portion **Topic** of the network, but we need to look closer at the rules that govern the interoperation between the 802.1D STP and PVST+, and the cooperation of PVST+ regions interconnected by CST regions. 

Cisco PVST+ running on trunks uses a VLAN 1 STP instance to communicate with nonCisco switches and their STP. VLAN 1’s STP instance in PVST+ regions interoperates and merges with the STP in CST regions. As a result, the entire switched network computes a single loop-free topology. In CST regions, the active loop-free topology is binding for all VLANs; inside PVST+ regions, the active loop-free topology applies to VLAN 1 only. Other VLANs inside PVST+ regions have their own PVST+ instances. 

PVST+ instances for VLANs other that VLAN 1 in PVST+ regions treat CST regions simply as loop-free shared segments. This is done by encapsulating the PVST+ BPDUs on 

Chapter 3: Spanning Tree Protocol  121 

**Key Topic** 

trunks differently than ordinary BPDUs: Their destination MAC address is set to the multicast address 0100.0CCC.CCCD (ordinary STP BPDUs are destined to 0180.C200.0000), they are tagged with the corresponding VLAN (ordinary STP BPDUs are untagged), and by using SNAP encapsulation (ordinary STP BPDUs use LLC encapsulation without SNAP). In addition, each PVST+ BPDU has a special TLV record placed at its end that carries the VLAN number in which the PVST+ BPDU was originated. We will call this TLV the Port VLAN ID TLV, or a PVID TLV. This TLV is analyzed by PVST+ switches and compared to the VLAN in which the BPDU is received to detect native VLAN mismatches. As a result, PVST+ BPDUs are tunneled across CST regions, with CST switches flooding them as ordinary multicasts without processing them. To non-VLAN 1 PVST+ instances, the entire switched network appears as PVST+ regions interconnected by shared segments. By tunneling PVST+ BPDUs across CST regions, PVST+ STP instances for VLANs 2–4094 in individual PVST+ regions cooperate together to form a single spanning tree for each corresponding VLAN inside all PVST+ regions, with CST regions merely serving the purpose of loop-free shared segments connecting the PVST+ regions together. 

VLAN 1 on PVST+ trunks is actually handled specially: Both standard STP BPDUs and PVST+ BPDUs are sent for VLAN 1. However, only the STP BPDU is used both by CST and PVST+ switches in VLAN 1 to compute the spanning tree. PVST+ BPDU for VLAN 1 is used to detect native VLAN mismatches and is otherwise ignored upon arrival. 

To summarize the sending and processing of PVST+ and ordinary IEEE BPDUs on ports, when _sending_ BPDUs, access ports send only IEEE BPDUs relevant to their access VLAN. Trunk ports always send a set of BPDUs: 

- IEEE-formatted BPDUs for VLAN1, always untagged. 

- PVST+ BPDUs (also called SSTP BPDUs in Cisco documents) for all existing and allowed VLANs including VLAN1, tagged accordingly to the native VLAN of the trunk; that is, BPDUs for the native VLAN won’t be tagged and all others will. Each of these PVST+ BPDUs carries the PVID TLV. 

When processing _received_ BPDUs, an access port must receive only IEEE BPDUs; otherwise a Type Inconsistent state is declared. These IEEE BPDUs will be processed by the STP instance for the access VLAN of the port. On trunk ports, the processing is a little more complex: 

- IEEE-formatted BPDUs will be immediately processed by the VLAN1 STP instance. 

- PVST+ BPDUs are processed according to this sequence of steps: 

   **1.** Assign the BPDU to the appropriate VLAN by looking at its 802.1Q tag. If the tag is present, the BPDU is assigned to the VLAN indicated by the tag. If the tag is not present, the BPDU is assigned to the native VLAN. 

   **2.** Check the PVID TLV in the BPDU. If the VLAN stored in the PVID TLV does not match the VLAN to which the BPDU was assigned, drop the BPDU and declare the PVID_Inconsistent state for the offending pair of VLANs. This is the native VLAN mismatch check. 

122  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**3.** BPDUs whose PVID TLV VLAN matches the assigned VLAN will be processed by STP in their appropriate VLANs except BPDUs for VLAN1. Because the information for VLAN1 is duplicated in the IEEE BPDUs and PVST+ BPDUs and the IEEE BPDUs always have to be processed, the PVST+ BPDU for VLAN1 served only the purpose of protection against native VLAN mismatch in VLAN1, and can be dropped afterward. 

Figure  3-7 shows a network in which three CST regions of non-Cisco switches connect to two regions of Cisco PVST+ supporting switches. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0163-03.png)


**----- Start of picture text -----**<br>
CST Region 1<br>Non-Cisco<br>.1Q CST Region 2<br>Non-Cisco<br>.1Q Common Non-Cisco<br>Non-Cisco<br>Spanning Tree<br>Non-Cisco Non-Cisco<br>STP only in<br>VLAN 1<br>PVST+ Region Non-native VLAN STP PVST+ Region<br>BPDUs trunked, sent to<br>0100.0CCC.CCCD<br>3560 ISL 3560 3560 ISL 3560<br>.1Q .1Q<br>.1Q .1Q .1Q .1Q<br>.1Q .1Q<br>2960 2960 2960 2960<br>Non-native VLAN STP<br>BPDUs trunked, sent to<br>0100.0CCC.CCCD<br>Non-Cisco Non-Cisco<br>CST Region 3<br>Non-Cisco<br>**----- End of picture text -----**<br>


**Figure 3-7** _Combining Standard IEEE 802.1Q and CST with PVST+_ 

The topology in  Figure  3-7 consists of three CST and two PVST+ regions. CST regions use ordinary STP with no per-VLAN semantics. PVST+ regions run STP independently in each VLAN, and on PVST+ boundaries, they use the VLAN 1 STP instance to interact and interoperate with CST regions. 

Chapter 3: Spanning Tree Protocol  123 

As CST and PVST+ VLAN 1 STP instances will interact and cooperate with each other, the result of this interaction is a tree that spans through the entire network. In CST regions, the loop-free topology will be shared by all VLANs; in PVST+ regions, the loopfree topology will be applied to VLAN 1 only. Assuming that the topmost switch in CST Region 2 is the root switch and all links have the same STP cost, the resulting loop-free topology in CST regions and in VLAN 1 in PVST+ regions is shown in  Figure  3-8 . 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0164-02.png)


**----- Start of picture text -----**<br>
CST Region 1<br>Non-Cisco<br>CST Region 2<br>Non-Cisco<br>.1Q Non-Cisco<br>Non-Cisco<br>Non-Cisco Non-Cisco<br>PVST+ Region PVST+ Region<br>3560 ISL 3560 3560 ISL 3560<br>.1Q<br>.1Q .1Q<br>.1Q<br>2960 2960 2960 2960<br>Non-Cisco Non-Cisco<br>CST Region 3<br>Non-Cisco<br>**----- End of picture text -----**<br>


**Figure 3-8** _Resulting Spanning Tree in CST Regions and in VLAN 1 in PVST+ Regions_ 

In simple terms, the result of CST and VLAN 1 STP interaction can be easily visualized simply by considering all switches to run a single STP instance and computing the spanning tree, ignoring all VLANs for the moment, then taking into consideration that in CST regions, this spanning tree will be shared by all VLANs, while in PVST+ regions, only VLAN 1 will be affected. Also, any CST region that interconnects two or more PVST+ regions is internally loop free and either continuous (as in CST Region 2; this region provides a transit connectivity between PVST+ regions) or partitioned (as in CST Region 3; this region does not provide transit connectivity to PVST+ regions). 

124  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

This observation about CST regions being internally loop free is important to understand the operation of remaining non-VLAN 1 STP instances in PVST+ regions. After loops have been eliminated from CST regions, the resulting network as seen by PVST+ STP instances can be seen in  Figure  3-9 . 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0165-02.png)


**----- Start of picture text -----**<br>
PVST+ Region Non-native VLAN STP PVST+ Region<br>BPDUs trunked, sent to<br>0100.0CCC.CCCD<br>3560 ISL 3560 3560 ISL 3560<br>.1Q .1Q<br>.1Q .1Q .1Q .1Q<br>.1Q .1Q<br>2960 2960 2960 2960<br>**----- End of picture text -----**<br>


**Figure 3-9** _Network as Perceived by Non-VLAN 1 PVST+ STP Instances_ 

As PVST+ BPDUs are effectively tunneled across CST regions, the CST regions simply appear as shared segments to non-VLAN 1 PVST+ STP instances. These shared segments are internally loop free and either interconnect PVST+ regions, in which case PVST+ will take care of eliminating any remaining possible loops between PVST+ regions, or do not even provide transit connectivity. PVST+ BPDUs will be flooded across the CST region without being processed. When forwarded PVST+ BPDUs reach the first Cisco PVST+ switch in the other PVST+ region, the switch, listening for multicasts to 0100.0CCC. CCCD, reads and interprets the BPDU. 

**Note** Along with 802.1s Multiple Spanning Tree Protocol (MSTP), 802.1Q allows 802.1Q trunks for supporting multiple STP instances. MST is covered later in this chapter.

## **STP Configuration and Analysis** 

Example  3-1 , based on  Figure  3-10 , shows some of the basic STP configuration and **show** commands. Take care to note that many of the upcoming commands allow the parameters to be set for all VLANs by omitting the VLAN parameter, or set per VLAN by including a VLAN parameter.  Example  3-1 begins with SW1 coincidentally becoming the root switch. After that, SW2 is configured to become root, and SW3 changes its Root Port as a result of a configured port cost in VLAN 1. 

Chapter 3: Spanning Tree Protocol  125

## Core Design 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0166-02.png)


**----- Start of picture text -----**<br>
Fa0/2 Fa0/1<br>SW1 SW2<br>Fa0/4 Fa0/3<br>Fa0/3 Fa0/4<br>Fa0/2 Fa0/1<br>Fa0/1 Fa0/2<br>SW3 Fa0/4 Fa0/3 SW4<br>**----- End of picture text -----**<br>


**Figure 3-10** _Network Used with  Example  3-1_ 

**Key Topic** 

**Example 3-1** _STP Basic Configuration and_ **show** _Commands_ 

! First, note the Root ID column lists the root's bridge ID as two parts, ! first the priority, followed by the MAC address of the root. The root cost of ! 0 implies that SW1 (where the command is executed) is the root. 

SW1# **sh spanning-tree root** 

Root    Hello Max Fwd Vlan                   Root ID          Cost    Time  Age Dly  Root Port ---------------- -------------------- --------- ----- --- ---  -----------VLAN0001         32769 000a.b7dc.b780         0    2   20  15 VLAN0011         32779 000a.b7dc.b780         0    2   20  15 VLAN0012         32780 000a.b7dc.b780         0    2   20  15 VLAN0021         32789 000a.b7dc.b780         0    2   20  15 VLAN0022         32790 000a.b7dc.b780         0    2   20  15 

! The next command confirms that SW1 believes that it is the root of VLAN 1. 

SW1# **sh spanning-tree vlan 1 root detail** Root ID    Priority    32769 Address     000a.b7dc.b780 This bridge is the root Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec 

! Next, SW2 is configured with a lower (better) priority than SW1, 

! so it becomes the root. Note that because SW2 is defaulting to use 

! the System ID Extension, the actual priority must be configured as a ! multiple of 4096. 

126  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

SW2# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. SW2(config)# spanning-tree vlan 1 priority ? <0-61440>  bridge priority in increments of 4096 SW2(config)# **spanning-tree vlan 1 priority 28672** SW2(config)# **^Z** SW2# **sh spanning-tree vlan 1 root detail** VLAN0001 Root ID    Priority    28673 Address     0011.92b0.f500 This bridge is the root Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec 

! The System ID Extension field of the bridge ID is implied next. The output 

! does not separate the 4-bit Priority field from the System ID field. The output 

! actually shows the first 2 bytes of the bridge ID, in decimal. For VLAN1, 

! the priority is 28,673, which is the configured 28,672 plus the VLAN ID, 

! because the VLAN ID value is used in the System ID field in order to implement 

! the MAC address reduction feature. The other VLANs have a base priority 

! of 32768, plus the VLAN ID - for example, VLAN11 has priority 32779, 

! (priority 32,768 plus VLAN 11), VLAN12 has 32780, and so on. 

SW2# **sh spanning-tree root priority** VLAN0001         28673 VLAN0011         32779 VLAN0012         32780 VLAN0021         32789 VLAN0022         32790 

! Below, SW3 shows a Root Port of Fa0/2, with cost 19. SW3 gets Hellos 

! directly from the root (SW2) with cost 0, and adds its default cost (19). 

! This next command also details the breakdown of the priority and system ID. 

SW3# **sh spanning-tree vlan 1** VLAN0001 Spanning tree enabled protocol ieee Root ID    Priority    28673 Address     0011.92b0.f500 Cost        19 Port        2 (FastEthernet0/2) Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec 

Chapter 3: Spanning Tree Protocol  127 

Bridge ID  Priority    32769  (priority 32768 sys-id-ext 1) Address     000e.837b.3100 Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec Aging Time 300 Interface        Role Sts Cost      Prio.Nbr Type ---------------- ---- --- --------- -------- -------------------------------Fa0/1            Altn BLK 19        128.1    P2p Fa0/2            Root FWD 19        128.2    P2p Fa0/4            Desg FWD 19        128.4    P2p Fa0/13           Desg FWD 100       128.13   Shr 

! Above, the port state of BLK and FWD for each port is shown, as well as the 

! Root Port and the Designated Ports. 

! Below, Switch3's VLAN 1 port cost is changed on its Root Port (Fa0/2), 

! causing SW3 to reconverge, and pick a new RP. 

SW3# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. SW3(config)# **int fa 0/2** SW3(config-if)# **spanning-tree vlan 1 cost 100** SW3(config-if)# **^Z** 

! The next command was done immediately after changing the port cost on 

! SW3. Note the state listed as "LIS," meaning Listening. STP has already 

! chosen Fa0/1 as the new RP, but it must now transition through Listening ! and Learning states. 

SW3# **sh spanning-tree vlan 1** VLAN0001 Spanning tree enabled protocol ieee Root ID    Priority    28673 Address     0011.92b0.f500 Cost        38 Port        1 (FastEthernet0/1) Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec Bridge ID  Priority    32769  (priority 32768 sys-id-ext 1) Address     000e.837b.3100 Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec Aging Time 15 

128  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Interface        Role Sts Cost      Prio.Nbr Type ---------------- ---- --- --------- -------- -------------------------------Fa0/1            Root LIS 19        128.1    P2p Fa0/2            Altn BLK 100       128.2    P2p Fa0/4            Desg FWD 19        128.4    P2p Fa0/13           Desg FWD 100       128.13   Shr 

The preceding example shows one way to configure the priority to a lower value to become the root. Optionally, the **spanning-tree vlan** _vlan-id_ **root** { **primary** | **secondary** } [ **diameter** _diameter_ ] command could be used. This command causes the switch to set the priority lower. The optional **diameter** parameter causes this command to lower the Hello, ForwardDelay, and MaxAge timers. (This command does not get placed into the configuration, but rather it acts as a macro, being expanded into the commands to set priority and the timers.) 

**Note** When using the **primary** option, the **spanning-tree vlan** command sets the priority to 24,576 if the current root has a priority larger than 24,576 or its priority is 24,576 and its MAC address is higher than the current switch’s MAC (that is, if setting the priority of 24,576 allows the current switch to become the root). Otherwise, this command sets this switch’s priority to 4096 less than the current root. With the **secondary** keyword, this switch’s priority is always set to 28,672. Also note that this logic applies to when the configuration command is executed; it does not dynamically change the priority if another switch later advertises a better priority.

## **Rapid Spanning Tree Protocol** 

IEEE 802.1w _Rapid Spanning Tree Protocol (RSTP)_ enhances the 802.1D standard with one goal in mind: improving STP convergence. Updates to the entire protocol operation are multifold and result in a dramatic increase of its convergence speed—well below 1 second in properly designed networks.

## **New Port Roles, States and Types, and New Link Types** 

RSTP has significantly reworked the classification of port and link properties to streamline and optimize its operation. Properties of ports include port _states_ , port _roles_ , and port _types_ . In addition, links interconnecting RSTP switches also have their _types_ . 

The number of port _states_ has been reduced from five to three: While 802.1D STP defines Disabled, Blocking, Listening, Learning, and Forwarding states, 802.1w RSTP defines only Discarding, Learning, and Forwarding states. Discarding and Forwarding states are stable states; Learning is a transitory state. This cleanup relates to the fact that a port can either be in stable state, that is, Forwarding or Discarding, for an unlimited time in the absence of any topological changes, or can be in a transitory Learning state, going 

Chapter 3: Spanning Tree Protocol  129 

from Discarding to Forwarding over a limited time period.  Table  3-5 compares the port states defined by each protocol. 

**Table 3-5** _RSTP and STP Port States_ 

**Key Topic** 

|**Table 3-5** _RSTP and S_|_TP Port States_||
|---|---|---|
|**Administrative State**|**STP State (802.1D)**|**RSTP State (802.1w)**|
|Disabled|Disabled|Discarding|
|Enabled|Blocking|Discarding|
|Enabled|Listening|Discarding|
|Enabled|Learning|Learning|
|Enabled|Forwarding|Forwarding|



In RSTP, a Discarding state means that the port does not forward data frames, receive data frames, or learn source MAC addresses, regardless of whether the port was shut down, failed, or simply does not have a reason to forward frames. Note that even a Discarding port, similarly to the Blocking state in legacy STP, continues to process received BPDUs; send BPDUs (depending on its role); and send and receive frames of inter-switch signaling protocols such as DTP, VTP, CDP, LLDP, PAgP, LACP, or LOOP. The Discarding is also the default state of a port that has newly come alive (with the exception of an Edge port whose default state is Forwarding). 

**Key Topic** 

RSTP decouples the state of the port from its purpose, or a _role_ , in a topology, and defines four separate port roles: 

- Root Port (maintains its usual meaning) 

- Designated Port (maintains its usual meaning) 

- Alternate Port (a prospective replacement for the switch’s own Root Port) 

- Backup Port (a prospective replacement for the switch’s own Designated Port into a shared segment) 

This decoupling allows for better definition of what function a port fulfills in a topology without inferring its role purely from its state. Also, this split underlines the fact that during transitory periods, Root and Designated Ports can be put into Discarding or Learning states, or—as is in the case of the Proposal/Agreement process—these can be skipped. Table  3-6 lists individual RSTP port roles, how they are determined, and their purpose. 

130  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 3-6** _RSTP Port Roles_ 

|**RSTP Role**|**Definition**|
|---|---|
|Root Port|Same as 802.1D Root Port.|
|Designated Port|Same as 802.1D Designated Port.|
|Alternate Port|A replacement Root Port. Alternate Ports are ports receiving BPDUs|
||from other switches but not meeting requirements to become Root or|
||Designated. Such a port is attached to a neighboring switch and provides|
||a possible alternate path toward the root. Upon the loss of the current|
||Root Port, the Alternate Port receiving the best resulting BPDUs will be|
||rapidly promoted to the role of Root Port and moved to the Forwarding|
||state.|
|Backup Port|A replacement Designated Port. Backup Ports are ports receiving|
||BPDUs from the same switch but not meeting requirements to become|
||Designated. Such a port is attached to the same link as another port on|
||the same switch, but the other port is Designated for that segment. The|
||Backup Port is ready to take over if the DP fails; however, this takeover is|
||not rapid. Rather, it is driven by timers.|



The Alternate Port concept offers protection against the loss of a switch’s Root Port, also called a _direct link failure_ , by keeping track of the Alternate Ports with a path to the root. If the current Root Port fails, RSTP will simply compare the resulting BPDUs (BPDUs stored on ports after incrementing the Root Path Cost by the receiving port’s cost) on Alternate Ports and choose the port with the superior resulting BPDU as the new Root Port. This port will be immediately declared Root Forwarding.  Figure  3-11 illustrates this process. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0171-04.png)


**----- Start of picture text -----**<br>
Root Sec. Root<br>Root Alternate<br>Port Port<br>**----- End of picture text -----**<br>


**Figure 3-11** _Use of Alternate Port to Replace Lost Root Port (Direct Link Failure)_ 

The Backup Port role provides protection against losing the Designated Port attached to a shared link when the switch has another physical port attached to the same shared LAN. As this is a shared link, there is no rapid convergence. After the Designated Port fails, all Backup Ports for the same link become Designated Discarding after missing three BPDUs in a row from the former Designated Port (expiry of Rapid Spanning Tree [RST] BPDUs will be described in the next section). Out of them, only a single port will remain Designated Discarding; the others will again revert to Backup Discarding after receiving the BPDU from the newly elected Designated Port. This new Designated Port 

Chapter 3: Spanning Tree Protocol  131 

**Key Topic** 

will gradually move from Discarding through Learning to Forwarding. As Proposals are not sent on ports connected to shared links, there is no way of safely moving a Backup Port to Designated rapidly. 

The default role for a port that has newly come alive is Designated. 

Finally, in RSTP, ports have _types_ : A port can be either an Edge or a Non-Edge port. This property is already well known thanks to the Cisco PortFast feature. An Edge Port immediately becomes Designated Forwarding after coming up. It still sends BPDUs but it expects not to receive any. Should a BPDU be received by an Edge port, this port will revert to the Non-Edge type and start operating as a common RSTP port. No commands will be removed from the configuration; only the runtime operational type of the port will change. The port will again become an Edge port after it goes down and comes up again, either through disconnect/reconnect or through shutting it down and reactivating. There is no reliable way of automatically detecting whether a port is an Edge or a NonEdge port. The default port type on Cisco Catalyst switches is Non-Edge. 

Regarding links, RSTP recognizes two _link types_ : 

- **Point-to-point link:** A link that connects an RSTP switch to at most one neighboring RSTP switch. 

- **Shared link:** A link that connects an RSTP switch to two or more neighboring switches. 

In most modern LAN designs with no hubs or non-STP switches that create a shared communication environment from RSTP’s viewpoint, all links would be of the point-topoint type. Most of RSTP’s improvements in its reaction speed are usable only on pointto-point links. On shared links, RSTP reverts to slow operation driven by timers similar to STP. There is no reliable way of detecting whether a link is point-to-point or shared. However, Catalyst switches try to be somewhat smart in this aspect: If a port negotiates half-duplex operation with its connected neighbor, the switch assumes that the neighbor is a hub (as hubs are incapable of supporting full-duplex), and it will consider the link type to be shared. If a port negotiates full-duplex operation, the switch will assume that the neighbor is a switch running RSTP, and will treat the link as point-to-point. Obviously, this decision process is just a guess and there are easily presentable situations where this logic fails (for example, running half-duplex on a point-to-point link between two switches because of some technical difficulties or peculiarities of the link, or having three or more RSTP switches interconnected by an unmanaged switch together that do not run STP). There is no one-to-one correspondence between the duplex mode and the link type. In cases this heuristic fails, the link type can be configured on a per-port basis using the **spanning-tree link-type** { **point-to-point | shared** } command. 

**Note** The default _port role_ and _port state_ are Designated Discarding—this is the combination of roles and states applied to a port at the moment it becomes live. The default _port type_ is Non-Edge. The default _link type_ depends on the duplex mode of the port—for full-duplex, it is point-to-point; for half-duplex, it is shared. 

132  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Changes to BPDU Format and Handling** 

In RSTP, there is only a single type of BPDU used both for building a loop-free topology and for topology change notification purposes. TCN BPDUs are not used by RSTP. For RSTP, the Protocol Version field is set to 2 (legacy STP uses Version 0; Version 1 was an STP variant for Remote MAC Bridging according to the 802.1G standard but was never widely deployed). 

The Flags field has been updated. In 802.1D STP BPDUs, only 2 bits out of 8 are used: TC (Topology Change) and TCA (Topology Change Acknowledgment). RSTP uses the 6 remaining bits as well to encode additional information: Proposal bit, Port Role bits, Learning bit, Forwarding bit, and Agreement bit. The TCA bit is not used by RSTP. This change allows implementing the Proposal/Agreement mechanism and also allows a BPDU to carry information about the originating port’s role and state, forming the basis of RSTP’s Dispute mechanism, protecting against issues caused by unidirectional links. 

In STP, Configuration BPDUs are originated by the root switch only. A nonroot switch **Key** does not originate its own Configuration BPDUs; rather, it waits for a BPDU to arrive on **Topic** its Root Port to relay it farther out its own Designated Ports after updating its contents. This delays an appropriate reaction to a sudden loss of received BPDUs on a port—their lack only indicates a problem somewhere between the root switch and the current switch. The switch needs to wait for MaxAge-MessageAge seconds for the BPDU stored on the Root Port to expire. In RSTP, each switch originates BPDUs on its own, with their contents nevertheless based on the information from the BPDU stored on the switch’s Root Port. RSTP BPDUs therefore become more similar to a Hello mechanism known from routing protocols. If a switch ceases to receive RSTP BPDUs on its port, it is certain that the problem is contained on the link between this switch and its neighbor. This allows RSTP switches to age out BPDUs much sooner—in a _3x Hello_ interval. Three missing Hellos in a row cause a port to age out the stored BPDU. The MessageAge field value no longer has an influence on BPDU’s expiry. Instead, it serves the role of a hop count. Any BPDU whose MessageAge is equal to or higher than its MaxAge will be discarded upon arrival. 

RSTP improves handling of inferior BPDUs sent by the designated switch on a segment. **Key** In STP, if a designated switch (that is, a switch having a Designated Port on a segment) **Topic** suddenly started sending BPDUs that are inferior to the BPDUs sent earlier, remaining switches on the segment would ignore them until the superior BPDU expired from their ports, which is after MessageAge-MaxAge seconds (values taken from the superior BPDU). In RSTP, an inferior BPDU originated by a designated switch on a segment is accepted right away, immediately replacing previously stored BPDUs on receiving ports of attached switches. In other words, if a designated switch on a segment suddenly sends an inferior BPDU, other switches on the segment will immediately accept it as if the superior stored BPDU expired just when the inferior BPDU arrived, and reevaluate their own port roles and states on the segment according to usual rules. This behavior allows a switch to rapidly react to a situation where the neighboring switch experiences a disruptive change in its own connectivity toward the root switch (this is called an _indirect link failure_ ). Consider the situation in  Figure  3-12 . 

Chapter 3: Spanning Tree Protocol  133 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0174-01.png)


**----- Start of picture text -----**<br>
2<br>My RP failed. I am<br>receiving no other Hellos.<br>1<br>I must be the root now!<br>Root<br>Link fails.<br>Port<br>4<br>Root Sec. Root<br>I am receiving Hellos with<br>Designated<br>Port  superior root BID.<br>I am no longer root, and<br>Root Alternate this is my root port.<br>Port Port<br>AccessSw 3<br>I am suddenly receiving worse Hellos<br>from my designated switch. Accepting<br>them right away. They are inferior to<br>even my own Hellos on this port.<br>I am now designated on this segment!<br>**----- End of picture text -----**<br>


**Figure 3-12** _Accepting Inferior BPDUs from Designated Switch (Indirect Link Failure)_ 

To better understand the need for this improvement, it is important to realize that if an inferior BPDU arrives from the designated switch, the designated switch or its own upstream switches must have encountered a change for the worse to their connectivity toward the root switch—the root path cost might have increased, or the Root Bridge ID itself might have changed to a higher value. If the root path cost has increased, the neighboring switch might no longer be using the shortest available path toward the root switch, and possibly, the next shortest path to the root switch might be through the current switch. If the Root Bridge ID has increased, the neighboring switch believes that the root switch has changed, but the true root switch might be different. In both cases, this inferior information has to be processed immediately to find out whether the neighboring switch has to be updated about the root switch’s identity or about a better path toward it. This is accomplished by accepting and processing the inferior BPDU, and running the usual sequence of steps: reevaluating the role of the switch (whether it should become the root switch itself), reevaluating the choice of a Root Port, and reevaluating roles of remaining ports. If the port toward the neighbor becomes Designated (before the change, it could only have been Root or Alternate), it will start sending BPDUs, thereby updating the neighbor about the root switch and the available root path cost.

## **Proposal/Agreement Process in RSTP** 

Improvements described so far allow a switch or its neighbors to rapidly recover from a _lost connectivity_ to the root switch. However, a connectivity disruption can also be caused by _adding a new link_ into the topology that causes one of the switches to reelect its Root Port and place it on the added link (that is, the added link provides a better path to the root switch). RSTP uses the Proposal/Agreement process on a point-to-point link to rapidly put such a link into operation without causing a temporary switching loop or significant interruptions in the communication.

## 134  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

If a newly added point-to-point link causes one of the attached switches to place its Root Port on this new link, the roles of remaining ports on this switch can move from Root or Alternate to Designated (the root path cost of this switch can decrease below the costs of its neighbors). As the neighboring switches might not yet be informed about the changes on this switch, they might still have some of their ports toward this switch in the Designated role, too. This would cause a switching loop. Therefore, a loop has to be prevented locally on the switch that is performing its Root Port changeover. In addition, after the neighboring switches are informed about the potentially decreased root path cost of this switch, they might also decide to change their Root Ports to point toward this switch, causing them to face the very same task as the current switch. An addition of a new link to the topology can therefore have a cascading effect of several switches updating their Root Ports, and this needs to be handled rapidly and in a loop-free manner. 

Preventing a switch from creating a switching loop by rapidly changing and activating its Root Port can be done by having this switch put all its Non-Edge Designated ports into Discarding state before the new Root Port is put into Forwarding state. Note that the Non-Edge Designated ports include those ports that have moved from old Root and Alternate roles to Designated after a superior resulting BPDU was received on the new Root Port and the switch reevaluated the roles of all ports. 

This procedure alone would allow a switch to rapidly change its Root Port while maintaining a loop-free topology, but at the same time, it would cause a major disruption in the communication because the switch is effectively isolated from the network: While its new Root Port might be made Forwarding, the upstream neighbor’s Designated Port on the added link is still in the Discarding or Learning state. In addition, all Non-Edge Designated ports on this switch have been put into the Discarding state as well to prevent a possible loop. To avoid waiting twice for the ForwardDelay timer, an explicit signaling scheme between the switches needs to be used, allowing them to confirm that it is safe to put a Designated Port into the Forwarding state. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0175-04.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


This signaling scheme is called _Proposal/Agreement_ . The _Proposal_ signifies the willingness of a port to become Designated Forwarding, while the _Agreement_ stands for permission to do so immediately. After a new link point-to-point link is added between two switches, ports on both ends will come up as Designated Discarding, the default role and state for a Non-Edge port. Any Designated Port in a Discarding or Learning state sends BPDUs with the Proposal bit set. Both switches will therefore attempt to exchange BPDUs with the Proposal bit set (or simply a Proposal), assuming that they have the right to be Designated. However, if one of the ports receiving a Proposal discovers that the Proposal constitutes the best received resulting BPDU, its role will change from Designated to Root (the state will remain Discarding yet). Other port roles on that switch will also be updated accordingly. Furthermore, a switch receiving a Proposal on its Root Port will immediately put all its Non-Edge Designated ports into a Discarding state. This operation is called _Sync_ . A switch in Sync state is now isolated from the network, preventing any switching loop from passing through it: Its Root Port is still in the Discarding state (and even if it was Forwarding, the neighboring Designated Port is still Discarding or Learning), and its own Designated Ports are intentionally moved to the Discarding state. Now it is safe to move the new Root Port to the Forwarding state and inform the upstream switch that it is now allowed to move its Designated Discarding or Learning 

Chapter 3: Spanning Tree Protocol  135 

port to the Forwarding state. This is accomplished by a switch sending a BPDU with the Agreement bit set (or simply an Agreement) through its Root Port after performing the Sync. Upon receiving an Agreement on its Designated Discarding or Learning port, the upstream switch will immediately move that port into the Forwarding state, completing the Proposal/Agreement exchange between two switches. 

As a result of the Proposal/Agreement and Sync operation, all Non-Edge Designated ports on the switch with the new Root Port have been moved to the Discarding state. Because all Designated Discarding and Designated Learning ports send Proposals, the Proposal/Agreement exchange has effectively moved from “above” the switch to “beneath” it (with respect to the root switch being at the “top” of the spanning tree), constituting the cascading effect of switches pairwise reevaluating their choice of Root Ports, expressing their willingness to have their Designated Ports made Forwarding rapidly (Proposals), and eventually receiving approvals to do so (Agreements). This process is illustrated in  Figure  3-13 , showing a wave-like sending of Proposals, performing Sync and generating Agreements in turn while pushing the Proposal/Agreement exchange downstream. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0176-03.png)


**----- Start of picture text -----**<br>
1<br>1<br>3 3<br>2 2<br>Sync Sync<br>4 4 4 4<br>6 6 6 6<br>5 5 5 5<br>Sync Sync Sync Sync<br>Proposal<br>Proposal<br>Agreement Agreement<br>Agreement<br>Proposal Proposal<br>Agreement Agreement<br>Proposal<br>Agreement<br>Proposal<br>**----- End of picture text -----**<br>


**Figure 3-13** _Proposal/Agreement Mechanism in RSTP_ 

**Note** Outages in a switched network can be caused by direct link failures (a switch losing its Root Port), indirect link failures (a neighbor losing its Root Port), adding a new root link, or a root switch changeover. RSTP has reaction mechanisms for each of these events: Direct link failures are handled by the best Alternate Port becoming a new Root Port, indirect link failures are handled by the concept of accepting inferior BPDUs from designated switches, adding a new root link is handled by the Proposal/Agreement mechanism, and the changeover of a root switch is handled by the combination of the mechanisms above. 

136  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Note** During the Proposal/Agreement exchange, all Non-Edge Designated ports will be moved to Discarding state (the Sync operation). If ports toward end hosts are not explicitly configured as Edge ports using the **spanning-tree portfast** port level command or the **spanning-tree portfast default** global level command (both have an effect on access ports only), they will become Discarding during Sync. Because end hosts are incapable of sending RSTP Agreements, these ports will require twice the ForwardDelay interval to become Forwarding again, and the end hosts will experience major connectivity outages. In RSTP, it is of crucial importance to configure ports toward end hosts as Edge ports; otherwise the performance of the network might be perceived as being even worse than with 802.1D STP.

## **Topology Change Handling in RSTP** 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0177-03.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


As opposed to STP, which recognizes four distinct events as topology change events, RSTP simplifies this concept: Only a transition of a Non-Edge port from a non-Forwarding state to the Forwarding state is considered a topology change event in RSTP. The reason is that a port that has newly become Forwarding can provide a better path to a set of MAC addresses than was previously available, and the CAM tables need to be updated. The loss of a Forwarding port is not a cause for topology change event anymore, as the set of MAC addresses previously learned on that port is definitely inaccessible unless some other port in the topology becomes Forwarding (which is handled as a topology change anyway) and possibly provides an alternate path toward them. 

The way of propagating topology change information has also changed. Instead of forwarding the information about a topology change using TCN BPDUs in a hop-by-hop fashion to the root switch and causing the root switch to send BPDUs with the TC flag set, RSTP switches immediately flood BPDUs with TC flag set. More precisely, a switch that _detects_ a topology change on a port (that is, one of its own Non-Edge ports transitions into the Forwarding state) or _learns_ about a topology change on a port (a BPDU with the TC flag set is received on its Root or Designated Port) will do the following: 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0177-06.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


- Set a so-called tcWhile timer to the value of the Hello time plus one second (older revisions of RSTP set this value to twice the Hello time) on all remaining Non-Edge Designated ports and Root Port if any, except the port on which the topology change was detected or learned. 

- Immediately flush all MAC addresses learned on these ports. 

- Send BPDUs with the TC flag set on these ports every Hello seconds until the tcWhile timer expires. 

This way, information about a topology change is rapidly flooded along the spanning tree in the form of BPDUs with the TC flag set, and causes switches to immediately flush their CAM tables for all ports except those ports on which the topology change was detected or learned, as they point in the direction of the topology change where a set of MAC addresses might have become reachable through a new or improved path. 

Chapter 3: Spanning Tree Protocol  137 

**Key Topic** 

Edge ports never cause a topology change event, and MAC addresses learned on them are not flushed during topology change event handling.

## **Rapid Per-VLAN Spanning Tree Plus (RPVST+)** 

RPVST+ is a form of running RSTP on a per-VLAN basis, analogous to PVST+. This provides the subsecond convergence of RSTP with the advantages of PVST+ described in the previous section. Thus, RPVST+ and RSTP share the same characteristics such as convergence time, Hello behavior, the election process, port states, and so on. RPVST+ is backwardly compatible with PVST+. Also the rules of interoperation of RPVST+ with CST regions running RSTP are the same. 

Configuring RPVST+ is straightforward. In global configuration mode, issue the **spanning-tree mode rapid-pvst** command. Also, it is very important to configure ports toward end hosts as Edge ports—either on a per-port basis using the **spanningtree portfast** command or globally using the **spanning-tree portfast default** command. Both these commands have an effect only on ports operating in access mode. Additionally, as explained earlier, most RSTP improvements are applicable only on pointto-point links. If the physical connections between switches are of the point-to-point nature but operate in half-duplex (abnormal for a correct point-to-point interconnection!), Cisco switches will treat these links as shared, as also evidenced by the acronym Shr in the **show spanning-tree** output. In these rare cases, if the link is truly point-to-point, the link type can be overridden using the **spanning-tree link-type point-to-point** interface level command. Apart from these specific configurations, all other configuration commands are of the same meaning as in PVST+. See the “Further Reading” section, later in this chapter, for a source of more information on RPVST+. 

**Note** For RSTP and consequently RPVST+ to provide rapid reaction to changes in the network topology, all switches must run RSTP or RPVST+, all inter-switch links must be properly installed and recognized as point-to-point links, and all ports toward end stations must be properly identified as edge ports. Failure to meet these three requirements will degrade the RSTP and RPVST+ performance, voiding its advantages. Ports toward legacy switches will revert to legacy 802.1D STP or PVST+ operation. On shared links, RSTP and RPVST+ revert to timers. On non-edge ports, RSTP and RPVST+ rely on the Proposal/Agreement procedure to provide rapid reaction, and if the neighboring device does not speak RSTP or RPVST+, it will not be able to send an Agreement in response to a Proposal.

## **Multiple Spanning Trees: IEEE 802.1s** 

IEEE 802.1s _Multiple Spanning Trees (MST)_ , sometimes referred to as _Multiple STP (MSTP)_ , defines a standards-based way to use multiple instances of STP in a network that uses 802.1Q VLANs. The following are some of the main benefits of 802.1s: 

- Like PVST+, it allows the tuning of STP parameters on a per-instance basis so that while some port blocks for one set of VLANs, the same port can forward in another set of VLANs. 

138  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

- As opposed to PVST+, it does not run a separate STP instance for each and every VLAN because that is largely unnecessary: Usually only a handful of different spanning trees is required and configured in a network. Running a separate STP instance for each VLAN in PVST+ merely results in multiple instances creating exactly the same spanning tree while consuming multifold system resources. Instead, MST runs in instances whose existence is not directly related to any particular VLAN. Instances are created by configuration, and VLANs are subsequently mapped onto them. Spanning tree created by an MST instance is shared by all VLANs mapped onto that instance. 

- Use 802.1w RSTP for rapid convergence in each instance, inheriting all its rapid convergence properties. The following advantages have been retained: general RSTP rules about BPDU expiry in a 3x Hello interval, acceptances of inferior BPDUs from designated switches, port roles/states/types, link types, Proposal/Agreement, and so on. 

- At press time, various Catalyst platforms have a limit on the maximum number of concurrent STP instances. The 2960, 3560, and 3750 platforms, for example, support at most 128 STP instances. If more than 128 VLANs are created and active on ports, some VLANs will not have any STP instance running and will not be protected against switching loops. If decreasing the number of active VLANs is not an option, neither PVST+ nor RPVST+ can be used, and MST is the only choice. 

- MST is the only standards-based and interoperable version of STP supporting VLANs and suitable in multivendor switched environments.

## **MST Principles of Operation** 

MST organizes the network into one or more _regions._ An MST region is a group of **Key** switches that together use MST in a consistent way—they run the same number of MST **Topic** instances and map the same sets of VLANs onto these instances, among other things. For example, in  Figure  3-14 , an MST region has been defined, along with connections to non-MST switches. Focusing on the left side of the figure, inside the MST region, you really need only two instances of STP—one each for roughly half of the VLANs. With two instances, the access layer switches will forward on their links to SW1 for one set of VLANs using one MST instance, and forward on their links to SW2 for the other set of VLANs using the second MST instance. 

One of the key benefits of MST over PVST+ is that it requires only one MST instance for a group of VLANs. If this MST region had hundreds of VLANs, and used PVST+, hundreds of sets of STP messages would be used. With MST, only one set of STP messages is needed for each MST instance. 

Chapter 3: Spanning Tree Protocol  139 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0180-01.png)


**----- Start of picture text -----**<br>
Non-MST Region Non-MST Region<br>Non-Cisco .1Q Non-Cisco Non-Cisco Non-Cisco<br>.1Q .1Q CST<br>Topology<br>MST Region<br>3560 ISL 3560<br>3560<br>Root Root<br>Instance1 Instance2<br>.1Q .1Q MST appears as a<br>.1Q .1Q single switch to the<br>outside world<br>FWD FWD<br>Instance1 Instance2<br>FWD<br>FWD<br>Instance1<br>Instance2<br>2960 2960<br>**----- End of picture text -----**<br>


**Figure 3-14** _MST Operations_ 

**Key Topic** 

MST reuses the concept of System ID Extension from IEEE 802.1t to embed the instance number into the Bridge ID. As the System ID Extension field contains 12 bits, the range of MST instance numbers is in the range of 0–4095, though at the time of this writing, different Catalyst platforms supported different ranges: 0–15 on Catalyst 2950, and 0–4094 on Catalyst 2960 and 3560. Furthermore, the MST standard allows for at most 65 active MST instances (instance 0 plus at most 64 user-definable instances). Apart from being higher than any reasonable network would require, this limit is also motivated by the fact that MST uses a _single_ BPDU to carry information about all instances, and it must fit into a single Ethernet frame. While a typical Ethernet MTU of 1500B would allow for approximately 88 MST instances in total, the limit of 64 user-definable in stances is sufficient for any practical needs and fits well into an ordinary Ethernet frame. In MST, a port sends BPDUs if it is Designated for at least one MST instance. As MST uses a single BPDU for all instances, it is possible to see both switches on a pointto-point link to send BPDUs to each other if each of these switches is Designated in a different MST instance. 

**Key Topic** 

Out of all MST instances, the instance 0 has a special meaning. This instance is also called the _Internal Spanning Tree_ , or IST, and serves several purposes. First, this instance always exists even if no other MST instances are created, providing a loop-free environment to VLANs mapped onto it within a region. Without any additional configuration, all VLANs are mapped onto the IST. Second, the IST is the only instance that interacts with STP run on switches outside the MST region. Whatever port role and state are determined by the interaction of IST on a region boundary with a neighboring switch, this role and state will be inherited by all existing VLANs on that port, not just by VLANs 

140  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

mapped onto the IST. This is a part of overall MST operations that makes the region appear as a single switch to other regions and non-MST switches. 

If the network consists of several MST regions, each of them can be visualized as a single switch. The view of the entire topology consisting of several MST regions can thus be simplified—instead of a region, imagine a single switch in its place while keeping the links interconnecting different regions in place. Obviously, the resulting network after this simplification can still contain loops if the regions are interconnected by redundant links. MST blocks these loops by building a so-called _Common Spanning Tree (CST)_ . This CST is simply a result of the interaction of individual ISTs on region boundaries, and constitutes a spanning tree between individual regions, consisting purely of links between MST regions. Also, if there was a non-MST (either STP or RSTP) part of the network, it would become an integral part of the CST. This CST has no per-VLAN semantics—it is a spanning tree interconnecting MST region boundaries and optionally spanning non-MST regions, shared by all VLANs. CST has two main purposes: 

- It determines loop-free paths between regions. An important consequence is that loops between regions are blocked on inter-region links and not inside regions, just like loops between switches would be blocked on the inter-switch links, not somewhere “inside” those switches. This behavior is consistent with the simplifying notion that from outside, an MST region can be perceived as just a single switch. 

- CST is the only spanning tree that can be understood and participated in by nonMST (that is, STP and RSTP) switches, facilitating the interoperation between MST and its predecessors. In mixed environments with MST and STP/RSTP, STP/RSTP switches unknowingly participate in CST. Costs in CST reflect only the costs of links between regions and in non-MST parts of the network. These costs are called _external costs_ by MST. 

In each MST region, the CST on the region’s boundary merges with the IST inside the **Key** region. The resulting tree consists of a loop-free interconnection between MST regions **Topic** “glued together” with loop-free interconnection inside each MST region, and is called the _Common and Internal Spanning Tree_ , or CIST. This tree is the union of CST between regions and ISTs inside individual regions, and is a single spanning tree that spans the entire switched topology. As each MST region has its own IST root, CIST—consisting of ISTs inside regions and CST between regions—can have multiple root switches as a result. These switches are recognized as the CIST Root Switch (exactly one for the entire CIST) and CIST Regional Root Switches (exactly one for the IST inside each region). CIST Regional Root Switch is simply a different name for an IST root switch inside a particular region. 

The CIST Root Switch is elected by the lowest Bridge ID from all switches that participate in CIST, that is, from all MST switches across all regions according to their IST Bridge IDs (composed of IST priority, instance number 0, and their base MAC address), and from all STP/RSTP switches, if present, according to the only Bridge IDs they have. If running a pure MST-based network, the CIST Root Switch will be the switch whose IST priority is the lowest (numerically), and in the case of a tie, the switch with the lowest base MAC address. This switch will also become the root of IST inside its own MST 

Chapter 3: Spanning Tree Protocol  141 

region; that is, it will also be the CIST Regional Root Switch. As the CIST Root Switch has the lowest known Bridge ID in the CST, it is automatically the CST Root as well, although this observation would be important only in cases of mixed MST and non-MST environments. 

In other MST regions that do not contain the CIST Root Switch, only MST switches at the region boundary (that is, having links to other regions) are allowed to assert themselves as IST root switches. This is done by allowing the CIST Regional Root ID to be set either to the Bridge ID of the switch itself if and only if the switch is also the CIST Root, or in all other cases, to the Bridge ID of an MST boundary switch that receives BPDUs from a different region. Remaining internal switches have therefore no way of participating in IST root elections. From boundary switches, IST root switches are elected first by their lowest _external root path cost_ to the CIST Root Switch. The external root path cost is the sum of costs of inter-region links to reach the region with the CIST Root Switch, or in other words, the CST cost of reaching the region with the CIST Root Switch; costs of links inside regions are not taken into account. In case of a tie, the lowest IST Bridge ID of boundary switches is used. Note that these rules significantly depart from the usual concept of the root switch having the lowest Bridge ID. In MST regions that do not contain the CIST Root Switch, the regional IST root switches might not necessarily be the ones with the lowest Bridge IDs. 

A CIST Regional Root Switch has a particular importance for a region: Its own CIST Root Port, that is, the Root Port to reach the CIST Root Switch outside the region, is called the Master port (this is an added port role in MST), and provides connectivity from the region toward the CIST Root for all MST instances inside the region.

## **Interoperability Between MST and Other STP Versions** 

To understand the interoperation between MST and other STP versions, we first need to have a look at the way MST interoperates with non-MST switches running pure IEEE 802.1D STP or 802.1w RSTP without any per-VLAN semantics (let us call them simply non-MST switches). These non-MST switches run a single STP instance for all VLANs and so all VLANs share the same single spanning tree in the non-MST part of the network. Whatever role and state a non-MST switch puts a port into, this role and state are shared by all VLANs on that port. If a non-MST switch is to interoperate with one or more neighboring MST switches, these MST switches must give the impression of running a single STP or RSTP to non-MST switches. Also, because STP and RSTP do not understand nor see into the workings of MST in individual instances inside an MST region, the entire MST region is a single “black box” to STP and RSTP. It is quite logical, then, to treat this single “black box” as a single huge switch. This single switch must speak a single instance of STP or RSTP on its boundary ports toward its non-MST neighbors, and whatever decisions are made about port roles and states on this boundary, they must apply to all VLANs. The non-MST switches accomplish this trivially by the very way they run IEEE STP/RSTP; the MST switches do this by speaking exclusively the MST instance 0, also called the IST, on boundary ports, formatted into ordinary STP or RSTP BPDUs, and applying the negotiated port roles and states on boundary ports to all 

142  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

VLANs on those ports. The MST instance 0 has a key role here—it speaks to non-MST neighbors and it processes BPDUs received from them. 

The interoperation between an MST region and an older IEEE STP variant is relatively straightforward. The non-MST region speaks a single STP/RSTP instance. The MST region uses the IST to speak on behalf of the entire region to non-MST neighbors on boundary ports. The resulting boundary port roles and states derived from the interaction of IEEE STP/RSTP and IST are binding for all VLANs. 

Interaction between MSTP and Cisco’s PVST+ is significantly more complex to understand. PVST+ regions by definition run one STP or RSTP instance for each active VLAN. It might be tempting at first to have each received PVST+ BPDU processed by the particular MST instance to which the respective VLAN is mapped. This idea is futile, however. There can be two or more VLANs mapped to the same MST instance that have completely different root bridges, root path costs, and so on in the PVST+ region. Which root bridge IDs, root path costs, and other STP attributes shall be taken into account by this MST instance, then? Clearly, the idea of doing any “smart” mapping between PVST+ and MST instances is not the way to go. 

Instead, the idea of interoperation between MST and PVST+ stems from the basic idea of interoperation between MST and IEEE STP/RSTP. For both MST and PVST+ regions, a _single_ representative is chosen to speak on behalf of the entire region, and the interaction between these two representatives determines the boundary port roles and states for all VLANs. Doing this is trickier than it seems, though. While the role and state of an MST boundary will be unconditionally imposed on all VLANs active on that port (that is how MST boundary ports work), PVST+ ports have independent roles and states for each VLAN. If a single representative MST instance is chosen to speak on behalf of an MST region, its information must be delivered to PVST+ switches in such a way that every PVST+ instance receives the same information to make an identical, _consistent_ choice. The word _consistent_ becomes very important—it describes a process where both MST and PVST+ in all their instances arrive at the same port role and state determination even though only a single MST instance and a single PVST+ instance directly interact with each other. The purpose of the _PVST Simulation_ mechanism is to allow for a consistent interoperation between MST and PVST+ regions. 

In the MST-to-PVST+ direction, the MST region again chooses the IST as the representative, with the goal of speaking IST information to all PVST+ instances using PVST+ BPDUs. To allow the PVST+ region to make an identical, _consistent_ decision based on IST’s attributes for all known VLANs, all PVST+ instances must receive the same IST information formatted in PVST+ BPDUs. Therefore, MST boundary ports replicate the IST’s BPDUs into PVST+ BPDUs for all active VLANs. This way, the MST supplies PVST+ neighbors with _consistent_ information in all VLANs. A PVST+ neighbor receiving these BPDUs on any single port will therefore make an identical, _consistent_ choice of that port’s role and state for all VLANs. 

In the opposite direction, MST takes the VLAN 1 as the representative of the entire PVST+ region, and processes the information received in VLAN 1’s BPDUs in IST. The boundary port’s role and state will be binding for all VLANs active on that port. However, MST must make sure that the boundary’s port role and state as determined by 

Chapter 3: Spanning Tree Protocol  143 

interaction with VLAN 1’s STP instance truly represent the choice that all other PVST+ instances would also make; that is, it must ascertain whether the result of IST’s interaction with VLAN 1’s STP instance is _consistent_ with the state of STP instances run in other VLANs. 

Let us analyze this in closer detail. The interaction of IST run on an MST boundary port and VLAN 1 PVST+ can basically result in three possible roles of the port: Designated, Root, or Non-Designated (whether that is Alternate or Backup is not relevant at this point). 

An MST boundary port will become a Designated Port if the BPDUs it sends out (carrying IST data) are superior to incoming VLAN 1 PVST+ BPDUs. A Designated boundary port will unconditionally become Forwarding for all VLANs, not just for VLAN 1. Therefore, to make sure that the other PVST+ instances make a _consistent_ decision, the boundary port must verify whether other PVST+ instances would also consider it to be a Designated Port. This is trivially accomplished by listening to all incoming PVST+ BPDUs and making sure that each of them is inferior to the boundary port’s own BPDUs. This forms our first PVST Simulation consistency criterion: 

_PVST+ BPDUs for all VLANs arriving at a Designated boundary port must be inferior to its own BPDUs derived from IST._ 

Conversely, an MST boundary port will become a Root Port toward the CIST root bridge if the incoming VLAN 1 PVST+ BPDUs are so superior that they not only beat the boundary port’s own BPDUs but also are the best VLAN 1 PVST+ BPDUs received on any of the boundary ports. Obviously, this situation implies that the CIST Root is located in the PVST+ region and it is the root switch for VLAN 1. A root boundary port will unconditionally become forwarding for all VLANs. Therefore, to make sure that the other PVST+ instances make a consistent decision, the boundary port must also act like a Root Port toward root bridges in all remaining VLANs. This in turn implies that the root bridges for these VLANs must also be located in the PVST+ region and the Root Port toward them is exactly this particular boundary port. A simple, yet sufficient condition to make this happen is to verify whether incoming PVST+ BPDUs for VLANs other than 1 are identical or even superior to incoming PVST+ BPDUs for VLAN 1. This forms our second consistency PVST Simulation criterion: 

_PVST+ BPDUs for VLANs other than VLAN 1 arriving at a root boundary port must be identical or superior to PVST+ BPDUs for VLAN 1._ 

Note that if System ID Extension is used, PVST+ BPDUs for different VLANs cannot be identical, and in fact, with the same priority on a PVST+ root switch for multiple VLANs, PVST+ BPDU for VLAN _x_ is inferior to BPDU for VLAN _y_ if _x>y_ . Therefore, to meet the second consistency criterion, priorities for PVST+ root switches in VLANs other than VLAN 1 must be lower by at least 4096 from the priority of the PVST+ VLAN 1 root switch. 

In both these cases, if the criterion for a particular port role is not met, the PVST Simulation process will declare a PVST Simulation inconsistency and will keep the port in the blocked state until the consistency criterion for the port’s role is met again. Older switches report the offending port as Root Inconsistent; recent switches use the PVST Simulation Inconsistent designation instead. 

144  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Finally, an MST boundary port will become a Non-Designated port if the incoming VLAN 1 PVST+ BPDUs are superior to its own BPDUs but not that superior to make this port a Root Port. A Non-Designated boundary port will unconditionally become Blocking for all VLANs. Therefore, to make sure that the other PVST+ instances make a consistent decision, the boundary port should verify whether also other PVST+ instances would consider it to be a Non-Designated port. This could be trivially accomplished by listening to all incoming PVST+ BPDUs and making sure that each of them is superior to the boundary port’s own BPDU; however, Cisco appears to have implemented a slight optimization here. If indeed this criterion was met, all PVST+ instances would consis tently consider this port to be a Non-Designated port and the port would be blocked according to its Non-Designated role. If, however, this criterion was not met, that is, at least one non-VLAN1 PVST+ BPDU was inferior to this port’s BPDU, the PVST Simulation inconsistency would be declared, and the port would be kept blocked. So in any case, the port will be blocked. Hence, for Non-Designated ports, there are no consistency checks performed because the port is blocked regardless. 

If it is necessary to operate a mixed MST and PVST+ network, it is recommended to make sure that the MST region appears as a root switch to all PVST+ instances by lowering its IST root’s priority below the priorities of all PVST+ switches in all VLANs. 

It is noteworthy to mention that if a Cisco MST switch faces a pure 802.1D STP or 802.1w RSTP switch, it will revert to the appropriate STP version on the interconnecting port, that is, STP or RSTP, according to the neighbor type. However, if a Cisco MST switch is connected to a PVST+ or RPVST+ switch, it will _always_ revert to PVST+. In other words, Cisco MST interoperates with RPVST+ regions using only PVST+, reverting to PVST+ operation on a region boundary. This is an implementor’s decision made to simplify the interworking between MST and RPVST+ regions—it requires less state to be stored and processed, particularly with respect to the Proposal/Agreement mechanism. 

**Note** PVST Simulation consistency criteria require that for an MST Boundary port toward a PVST+ region to be Forwarding, one of the following conditions must be met: 

- Either the boundary port’s own IST BPDUs are superior to all received PVST+ BPDUs regardless of their VLAN (in this case, the port becomes Designated; “if be Designated Port for VLAN 1, then be Designated Port for all VLANs”) 

- Or the boundary port’s own IST BPDUs are inferior to received PVST+ BPDUs for VLAN 1, and _they_ are in turn identical or inferior to received PVST+ BPDUs for other VLANs (in this case, the port becomes Root Port; “if be Root Port for VLAN 1, then be Root Port for all VLANs”)

## **MST Configuration** 

Configuring MST requires a certain degree of prior planning. First, it is necessary to decide whether multiple regions shall be used and where their boundaries shall be placed. Multiple regions allow having independent numbers of MST instances, VLAN-to-instance 

Chapter 3: Spanning Tree Protocol  145 

mappings, and individual instance roots in each region. The overall network operation can become more complex to understand and maintain, though. Each region must be subsequently assigned its name, configuration revision number, and VLAN-to-instance mapping table. The name, revision number, and VLAN-to-instance mappings are three mandatory elements of MST configuration and must match on all switches of a single region. The name and configuration revision number are carried in MST BPDUs in their plain form. Instead of transmitting the entire VLAN-to-instance mapping table, an MD5 hash is performed over it and its value is carried in MST BPDUs. The region name, revision number, and the MD5 hash of the VLAN-to-instance mapping table are compared upon BPDU arrival and must match for two switches to consider themselves being in the same region. The hash value can be displayed using the **show spanning-tree mst configuration digest** EXEC command. On older switches, the **digest** keyword might be hidden but nevertheless accepted if typed in its entirety. 

A modification to the MST region configuration (name, revision, mapping of VLANs onto instances) on a single switch causes the switch to create its own region and trigger a topology change, possibly causing a transient network outage. Upgrading an MST region to a new configuration will therefore require a maintenance window. As changes to VLAN-to-instance mappings are most common, it is recommended to premap VLANs into instances even before the VLANs are created. Creating (or deleting) a VLAN after it is mapped to an instance will not cause any topology change event with respect to MST. 

If it is necessary to operate a mixed MST and PVST+ network, it is recommended to make sure that the MST region becomes the region containing the CIST Root Switch. This can be accomplished by lowering the IST root switch’s priority (that is, the priority of the existing root of instance 0 in the MST region) below the priorities of all PVST+ switches in all VLANs. 

Finally, older Cisco switches have implemented a prestandard version of MST that differs in the BPDU format and some other details. A quick test to verify whether the switch supports the standard or prestandard MST version is to issue the **show spanning-tree mst configuration digest** command. If there is only a single MD5 digest displayed in the output, the switch supports prestandard MST only. If there are two MD5 digests displayed, the switch supports standard MST and also the prestandard MST for backward compatibility. If a switch implementing standard MST is to be connected to a switch running prestandard MST, the port toward the prestandard switch must be configured with the **spanning-tree mst pre-standard** command; otherwise, permanent switching loops can ensue or the switch will keep the port blocking until configured with this command. 

Configuration of MST can be accomplished by following these steps: 

- **Step 1.** Enter MST configuration mode by using the **spanning-tree mst configuration** command. 

- **Step 2.** From MST configuration mode, create an MST region name (up to 32 characters) by using the **name** subcommand. 

- **Step 3.** From MST configuration mode, define an MST revision number by using the **revision** command. 

146  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

- **Step 4.** From MST configuration mode, map VLANs to an MST STP instance by using the **instance** command. 

- **Step 5.** From MST configuration mode, after reviewing the MST configuration before performing the changes using the **show current** command and after the changes using the **show pending** command, you can either apply the changes using the **exit** command or cancel the changes using the **abort** command. Both commands will exit from the MST configuration mode. 

- **Step 6.** Globally enable MST using the **spanning-tree mode mst** command. 

Example  3-2 demonstrates configuring a switch with an MST region. 

**Example 3-2** _MST Configuration and_ **show** _Commands_ 

**Key Topic** ! First, the MST region configuration is entered, defining the name of the region ! to be CCIE, the configuration revision to 1, and creating four instances ! with different VLANs mapped onto them. Note that the VLANs do not need to be ! created at all; they can be pre-mapped into MST instances and created later. ! The **show current** shows the current (empty at the moment) MST configuration, ! the **show pending** shows the modified but still unapplied configuration. SW1(config)# **spanning-tree mst configuration** SW1(config-mst)# **name CCIE** SW1(config-mst)# **revision 1** SW1(config-mst)# **instance 1 vlan 1-500** SW1(config-mst)# **instance 2 vlan 501-1000** SW1(config-mst)# **instance 3 vlan 1001-2047** SW1(config-mst)# **instance 4 vlan 2048-4094** SW1(config-mst)# **show current** Current MST configuration Name      [] Revision  0     Instances configured 1 Instance  Vlans mapped --------  --------------------------------------------------------------------0         1-4094 ------------------------------------------------------------------------------SW1(config-mst)# **show pending** Pending MST configuration Name      [CCIE] Revision  1     Instances configured 5 Instance  Vlans mapped --------  --------------------------------------------------------------------0         none 1         1-500 

Chapter 3: Spanning Tree Protocol  147 

2         501-1000 3         1001-2047 4         2048-4094 ------------------------------------------------------------------------------- 

SW1(config-mst)# **exit** 

SW1(config)# **spanning-tree mode mst** 

! To modify the switch's priority, **spanning-tree mst** _instance_ **priority** command 

! must be used instead of **spanning-tree vlan** _vlan-id_ **priority** . Also, modifying 

! a port's cost or priority is accomplished using **spanning-tree cost mst** and 

! **spanning-tree port-priority mst** commands instead of their counterparts utilizing 

! the **vlan** keyword. They have no effect in MST mode. 

SW1(config)# **spanning-tree mst 0 priority 0** SW1(config)# **spanning-tree mst 1 priority 4096** SW1(config)# **spanning-tree mst 2 priority 8192** 

! If switches in the region support VTPv3 then VTPv3 can be used to synchronize 

! the MST region configuration across all switches in the VTP domain. As all 

! switches in the VTP domain will share the same MST region configuration, they 

! will all become members of the same MST region. Hence, there is a 1:1 relation 

! between a VTPv3 domain and the MST region. 

SW1(config)# **vtp domain CCIE** 

Changing VTP domain name from NULL to CCIE 

*Mar 12 16:12:14.697: %SW_VLAN-6-VTP_DOMAIN_NAME_CHG: VTP domain name changed to CCIE. 

SW1(config)# **vtp version 3** 

SW1(config)# 

*Mar 12 16:12:18.606: %SW_VLAN-6-OLD_CONFIG_FILE_READ: Old version 2 VLAN configuration file detected and read OK.  Version 3 

files will be written in the future. 

SW1(config)# **vtp mode server mst** 

Setting device to VTP Server mode for MST. 

SW1(config)# **do vtp primary mst** 

This system is becoming primary server for feature  mst 

No conflicting VTP3 devices found. 

Do you want to continue? [confirm] 

*Mar 12 16:12:46.422: %SW_VLAN-4-VTP_PRIMARY_SERVER_CHG: 0023.ea41.ca00 has become the primary server for the MST VTP feature SW1(config)# 

! From this moment on, the entire **spanning-tree mst configuration** section will be ! synchronized across the entire VTPv3 domain, and changes to its contents on SW1 

148  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

! as the primary server switch will be propagated to all switches in the domain. 

! Note that MST region configuration revision is independent of VTPv3 revision 

! number and will not be incremented by VTP automatically. VTP uses its own 

! revision number which will be incremented.

## **Protecting and Optimizing STP** 

This section covers several switch configuration tools that protect STP from different types of problems or attacks, depending on whether a port is a trunk or an access port. 

The previous edition of this book covered Cisco-proprietary extensions to legacy STP— the UplinkFast and BackboneFast features. These additions have been dropped from the current exam blueprint, and in addition, their core ideas (tracking Alternate Ports, accepting inferior BPDUs from designated switches) have been leveraged in RSTP and MST, becoming an integral part of their design.

## **PortFast Ports** 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0189-09.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


The PortFast is a well-known improvement in legacy STP and PVST+, and is a standardized enhancement in RSTP and MST. Essentially, it defines an Edge port. We will use both _Edge port_ and _PortFast port_ terms interchangeably. An Edge port becomes forwarding immediately after coming up, does not generate topology change events, does not flush MAC addresses from the CAM table as a result of topology change handling, and is not influenced by the Sync step in the Proposal/Agreement procedure. An Edge port sends BPDUs but it expects not to receive any BPDUs back. If a BPDU does arrive at a PortFast port, the operational PortFast status will be disabled on the port until it goes down and back up. 

The use of PortFast on ports toward end hosts is important for several reasons. First and foremost, it accelerates the port’s transition into the Forwarding state. Apart from saving twice the ForwardDelay time, it also remediates problems with overly sensitive DHCP clients on end hosts that report an error if no response from a DHCP server is received within a couple of seconds. Second, a somewhat less obvious but far more grave reason to use PortFast is that in RSTP and MST, it prevents a port from being put into the Discarding state during Proposal/Agreement handling. Not taking care to configure Edge ports in a network running RSTP or MST will result in intermittent connectivity during topology changes, and while the network itself will reconverge in seconds at most (and usually much sooner), end hosts will suffer an outage for twice the ForwardDelay time. 

PortFast ports can be configured either directly on ports using the **spanning-tree portfast** command or on a global level using the **spanning-tree portfast default** command. Both of these commands apply only to ports operating in access mode (that is, static access or dynamic mode that negotiated an access link). This behavior simply follows the logic that end hosts are usually connected to access ports while links to other 

Chapter 3: Spanning Tree Protocol  149 

switches operate as trunks. If PortFast is enabled globally, but some access port is nevertheless connected to another switch, PortFast can be explicitly disabled on that port using the **spanning-tree portfast disable** command. 

If a trunk port is connected to an end device, such as a router or a server, it can be forced into PortFast mode using the **spanning-tree portfast trunk** interface level command. Be sure, however, to never activate PortFast on ports toward other switches. RSTP and MST will take care of their rapid handling if the other switch also speaks RSTP or MST.

## **Root Guard, BPDU Guard, and BPDU Filter: Protecting Access Ports** 

Network designers probably do not intend for end users to connect a switch to an access port that is intended for attaching end-user devices. However, it happens—for example, someone just might need a few more ports in the meeting room down the hall, so he figures that he could just plug a small, cheap switch into the wall socket. 

The STP topology can be changed based on one of these unexpected and undesired switches being added to the network. For example, this newly added and unexpected switch might have the lowest Bridge ID and become the root. To prevent such problems, BPDU Guard and Root Guard can be enabled on these access ports to monitor for incoming BPDUs—BPDUs that should not enter those ports, because they are intended for single end-user devices. Both features can be used together. Their base operations are as follows: 

- **BPDU Guard:** Enabled per port or globally per PortFast-enabled ports; error disables the port immediately upon receipt of any BPDU. 

- **Root Guard:** Enabled per port; ignores any received superior BPDUs to prevent this port from becoming the Root Port. Upon receipt of superior BPDUs, this switch puts the port in a root-inconsistent blocking state, ceasing forwarding and receiving data frames until the superior BPDUs cease. 

**Key Topic** 

The BPDU Guard can either be activated unconditionally on a per-port basis using the **spanning-tree bpduguard enable** interface command or globally using the **spanningtree portfast bpduguard default** command. The global command, however, activates the BPDU Guard only on ports that operate as PortFast ports (it does not matter how the port was configured for PortFast operation). Again, in the case where BPDU Guard is enabled globally but it needs to be deactivated on a particular PortFast port, the **spanning-tree bpduguard disable** interface command can be used. 

There is often confusion regarding the relation of PortFast and BPDU Guard to each other. In reality, the _only_ dependence between these mechanisms is concerned with configuring the BPDU Guard on a global level. In this case, it will be automatically activated on those ports on which PortFast is also active; in other words, the global activation of BPDU Guard will activate it on all Edge ports. Besides this particular _configurational_ 

150  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

dependency, PortFast and BPDU Guard are completely independent. On a port, BPDU Guard can be configured regardless of PortFast. PortFast, either per-port or globally, can be configured regardless of BPDU Guard. 

Regardless of how the BPDU Guard is activated on an interface, when a BPDU is received on such a port, it will be immediately err-disabled.

## **Key Topic** 

Root Guard can be activated only on a per-port basis using the **spanning-tree guard root** interface command. 

With BPDU Guard, the port does not recover from the _err-disabled_ state unless additional configuration is added. You can tell the switch to change from the err-disabled state back to an up state after a certain amount of time. With Root Guard, the port recovers automatically when the undesired superior BPDUs are no longer received for the usual MaxAge-Message age in STP, or 3x Hello in RSTP (effectively, when they expire). 

The BPDU Filter feature is concerned with stopping the transmission, and optionally the reception as well, of BPDUs on a port. Its behavior differs depending on how it is activated: 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0191-07.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


- If configured globally using **spanning-tree portfast bpdufilter default** , it applies only to Edge ports (that is, to ports on which PortFast is active). After these ports are connected to, they will start sending BPDUs each Hello interval; however, if during the next ten Hello intervals, no BPDU is received from the connected device, the port will stop sending BPDUs itself. As a result, the port will send only 11 BPDUs (one immediately after the port comes up, and then ten more during the ten Hello intervals) and then cease sending BPDUs. The port is still prepared to process any incoming BPDUs. If a BPDU arrives at any time, during the first ten Hello intervals or anytime after, BPDU Filter will be operationally deactivated on that port, and the port will start sending and receiving BPDUs according to usual STP rules. BPDU Filter operation on this port will be reinstated after the port is disconnected and reconnected. As usual, if the global configuration of BPDU Filter applies to an Edge port on which you do not want BPDU Filter to be activated, you can exempt the port using the **spanning-tree bpdufilter disable** command. 

- If configured locally on a port using the **spanning-tree bpdufilter enable** command, BPDU Filter will cause the port to unconditionally stop sending and receiving BPDUs altogether. 

The use of BPDU Filter depends on how it is configured. The global BPDU Filter configuration causes Edge ports to stop sending BPDUs after a certain time, assuming that it is not useful to send BPDUs to end devices as they do not speak STP. If it is discovered that such a port is actually connected to a switch by receiving a BPDU, the BPDU Filter will be deactivated on the port until the port goes down and comes back up (through disconnect/reconnect, or through shutting it down and activating it again). This can be considered an optimization in networks with many access ports toward end devices. 

Chapter 3: Spanning Tree Protocol  151 

BPDU Filter configured directly on a port causes the port to stop sending and processing received BPDUs. No BPDUs will be sent; received BPDUs will be silently dropped. This configuration prevents STP from participating with any other switch on the port. Usually, this feature is used to split a network into separate independent STP domains. Because in this case, STP does not operate over these ports, it is unable to prevent a switching loop if the STP domains are redundantly interconnected. It is the responsibility of the administrator, then, to make sure that there are no physical loops between the STP domains. 

Again, there is often confusion regarding the dependence of PortFast and BPDU Filter. Their true dependence is practically identical to that of BPDU Guard and PortFast. The _only_ situation where BPDU Filter and PortFast are _configurationally_ dependent is when BPDU Filter is configured on a global level, because in that case it automatically applies to all Edge ports (that is, ports with active PortFast). If a port on which BPDU Filter is active because global configuration (meaning that it must have been an Edge port) receives a BPDU, it will lose its Edge status, and because the global BPDU Filter configuration applies to Edge ports, BPDU Filter on this port will be deactivated as well. Apart from this, no other dependency between BPDU Filter and BPDU Guard exists. 

It is possible to combine globally configured BPDU Filter with BPDU Guard (the BPDU Guard can be also configured globally or per-port in this case). Should a port protected both with global BPDU Filter and BPDU Guard receive a BPDU, it will be automatically err-disabled. 

On the other hand, it does not make sense to combine port-level BPDU Filter with BPDU Guard. As the port drops all received BPDUs, the BPDU Guard will never see them, meaning that it will never be able to put the port into an err-disabled state.

## **Protecting Against Unidirectional Link Issues** 

Unidirectional links are links for which one of the two transmission paths on the link has failed, but not both. This can happen as a result of miscabling, cutting one fiber cable, unplugging one fiber, GBIC problems, or other reasons. Because STP monitors incoming BPDUs to know when to reconverge the network, adjacent switches on a unidirectional link could both become Forwarding, causing a loop, as shown in  Figure  3-15 . 

Figure  3-15 shows the fiber link between SW1 and SW2 with both cables. SW2 starts in a Blocking state, but as a result of the failure on SW1’s transmit path, SW2 ceases to hear Hellos from SW1. SW2 then transitions to the Forwarding state, and now all trunks on all switches are Forwarding. Even with the failure of SW1’s transmit fiber, frames will now loop counterclockwise in the network. 

On Catalyst switches, there are several mechanisms available to detect and avoid issues caused by unidirectional links. These mechanisms include UDLD, STP Loop Guard, Bridge Assurance, and the RSTP/MST Dispute mechanism. 

Unidirectional Link Detection (UDLD), a Cisco-proprietary Layer 2 messaging protocol, serves as an echo mechanism between a pair of devices. Using UDLD messages, each switch advertises its identity and port identifier pair as the message originator, and a list 

152  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

of all neighboring switch/port pairs heard on the same segment. Using this information, a unidirectional link can be detected by looking for one of the following symptoms: 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0193-02.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


- UDLD messages arriving from a neighbor do not contain the exact switch/port pair matching the receiving switch and its port in the list of detected neighbors. This suggests that the neighbor either does not hear this switch at all (for example, a cut fiber) or the neighbor’s port sending these UDLD messages is different from that neighbor’s port receiving this switch’s own UDLD messages (for example, a Tx fiber plugged into a different port than the Rx fiber). 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0193-04.png)


**----- Start of picture text -----**<br>
One Trunk, Two Fiber Cables<br>DP 1 3<br>FWD 2 Non-DP No more Hellos. I must<br>Tx Hello Cost 19 BLK be the DP. Let me<br>transition to forwarding!<br>SW1 SW2<br>Rx<br>RP RP<br>FWD FWD<br>DP<br>FWD DP<br>FWD<br>Root SW3<br>**----- End of picture text -----**<br>


**Figure 3-15** _STP Problems with Unidirectional Links_ 

- UDLD messages arriving from a neighbor contain the same switch/port originator pair as used by the receiving switch. This suggests a self-looped port. 

- A switch has detected only a single neighbor but that neighbor’s UDLD messages contain more than one switch/port pair in the list of detected neighbors. This suggests a shared media interconnection with an issue in its capability to provide full visibility between all connected devices. 

If any of these symptoms are detected, UDLD will declare the link as unidirectional and will _err-disable_ the port. 

In addition, a unidirectional link can under circumstances also manifest itself by sudden loss of all incoming UDLD messages without the port going down. This symptom is not always a reliable indication of a unidirectional link, though. Assume, for example, two switches interconnected by a link utilizing a pair of metallic/optical media converters. If one switch is turned off, the other switch will not experience a link down event; just the UDLD messages stop arriving. Assuming that the link has become unidirectional would be presumptuous in this case. 

UDLD therefore has two modes of operation with the particular respect to the sudden **Key** loss of arriving UDLD messages. In the _normal_ mode, if UDLD messages cease being **Topic** received, a switch will try to reconnect with its neighbors (eight times), but if this attempt 

Chapter 3: Spanning Tree Protocol  153 

**Key Topic** 

**Key Topic** 

fails, UDLD takes absolutely no action. In particular, the port that stopped receiving UDLD messages will remain up. In the _aggressive_ mode, after UDLD messages stop arriving, a switch will try eight times to reconnect with its neighbors, and if this attempt fails, UDLD will err-disable the port. The difference between the normal and aggressive mode therefore lies in the reaction to the sudden loss of incoming UDLD messages, that is, to an _implicit_ indication of a possible unidirectional link condition. Note that both normal and aggressive modes will err-disable the port if the unidirectional link is _explicitly_ detected by the three symptoms described earlier. 

UDLD can be activated either on a global level or on a per-port basis, and needs to be activated on both interconnected devices. Global UDLD configuration applies only to fiber ports; per-port UDLD configuration activates it regardless of the underlying media type. On the global level, UDLD is activated with the **udld** { **enable | aggressive** } command, the **enable** keyword referring to the normal mode and **aggressive** referring to the aggressive mode. On a port, UDLD is activated using the **udld port** [ **aggressive** ] command. If the **aggressive** keyword is omitted, normal mode is used. Operational status of UDLD including port information and detected neighbors and their states can be displayed using **show udld** and **show udld neighbors** commands. If UDLD err-disables a port after detecting a unidirectional link condition, apart from shutting it down and bringing it back up to reactivate it, a port can also be reset from the privileged EXEC mode using the **udld reset** command. 

STP Loop Guard is an added logic related to receiving BPDUs on Root and Alternate Ports on point-to-point links. In the case of a unidirectional link, these ports could move from Root or Alternate to Designated, thereby creating a switching loop. STP Loop Guard assumes that after BPDUs were being received on Root and Alternate Ports, it is not possible in a correctly working network for these ports to suddenly stop receiving BPDUs without them actually going down. A sudden loss of incoming BPDUs on Root and Alternate Ports therefore suggests that a unidirectional link condition might have occurred. 

Following this logic, STP Loop Guard prevents Root and Alternate Ports from becoming Designated as a result of total loss of incoming BPDUs. If BPDUs cease being received on these ports and their stored BPDUs expire, Loop Guard will put them into a _loopinconsistent_ blocking state. They will be brought out of this state automatically after they start receiving BPDUs again. 

Loop Guard can be activated either globally or on a per-port basis, and is a local protection mechanism (that is, it does not require other switches to be also configured with Loop Guard to work properly). If activated globally using the **spanning-tree loopguard default** command, it automatically protects all Root and Alternate Ports on STP point-topoint link types on the switch. Global Loop Guard does not protect ports on shared type links. It can also be configured on a per-port basis using the **spanning-tree guard loop** command, in which case it applies even to ports on shared links. 

The Bridge Assurance, applicable only with RPVST+ and MST and only on point-to-point links, is a further extension of the idea used by Loop Guard. Bridge Assurance modifies the rules for sending BPDUs. With Bridge Assurance activated on a port, this port 

**Key Topic** 

154  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

_always_ sends BPDUs each Hello interval, whether it is Root, Designated, Alternate, or Backup. BPDUs thus essentially become a Hello mechanism between pairs of interconnected switches. A Bridge Assurance–protected port is absolutely required to receive BPDUs. If no BPDUs are received, the port will be but into a _BA-inconsistent_ blocking state until it starts receiving BPDUs again. Apart from unidirectional links, Bridge Assurance also protects against loops caused by malfunctioning switches that completely stop participating in RPVST+/MST (entirely ceasing to process and send BPDUs) while opening all their ports. At the time of this writing, Bridge Assurance was supported on selected Catalyst 6500 and Nexus 7000 platforms. Configuring it on Catalyst 6500 Series requires activating it both globally using **spanning-tree bridge assurance** and on ports on STP point-to-point link types toward other switches using the **spanning-tree portfast network** interface command. The neighboring device must also be configured for Bridge Assurance. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0195-02.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


The Dispute mechanism is yet another and standardized means to detect a unidirectional link. Its functionality is based on the information encoded in the Flags field of RST and MST BPDUs, namely, the role and state of the port forwarding the BPDU. The principle of operation is very simple: If a port receives an inferior BPDU from a port that claims to be Designated Learning or Forwarding, it will itself move to the Discarding state. Cisco has also implemented the Dispute mechanism into its RPVST+. The Dispute mechanism is not available with legacy STP/PVST+, as these STP versions do not encode the port role and state into BPDUs. The Dispute mechanism is an integral part of RSTP/MST and requires no configuration.

## **Configuring and Troubleshooting EtherChannels** 

EtherChannel, also known as Link Aggregation, is a widely supported and deployed technology used to bundle several physical Ethernet links interconnecting a pair of devices into a single logical communication channel with increased total throughput. After an EtherChannel is established, it is represented to the devices as a single logical interface (called _Port-channel_ in Cisco parlance), utilizing the bandwidth of all its member links. This allows for traffic load sharing between the member links, taking advantage of their combined bandwidth. Also, should a link in an EtherChannel bundle fail, the traffic will be spread over remaining working links without further influencing the state of the logical interface. Control plane protocols that see only the logical Port-channel interface and not its underlying physical members, such as STP, will only notice a change in the interface’s bandwidth parameter (if not configured statically using the **bandwidth** command). The reaction to a failure or addition of a member link is therefore significantly more graceful than a reaction to a loss or reestablishment of a standalone link. 

**Key Topic**

## **Load Balancing Across Port-Channels** 

EtherChannel increases the available bandwidth by carrying multiple frames over multiple links. A single Ethernet frame is always transmitted over a single link in an EtherChannel bundle. A hashing function performed over selected frames’ address fields produces a number identifying the physical link in the bundle over which the frame will 

Chapter 3: Spanning Tree Protocol  155 

be forwarded. The sequence of frames having an identical value in a particular address field (or a set of fields) fed into the hashing function is called a _conversation_ or simply a _flow_ . This hashing function is deterministic, meaning that all frames in a single flow produce the same hash value, and are therefore forwarded over the same physical link. Hence, the increase in the available bandwidth is never experienced by a single flow; rather, multiple flows have a chance of being distributed over multiple links, achieving higher aggregated throughput. The fact that a single flow is carried by a single link and thus does not benefit from a bandwidth increase can be considered a disadvantage; however, this approach also prevents frames from being reordered. This property is crucial, as EtherChannel—being a transparent technology—must not introduce impairments that would not be seen on plain Ethernet. 

Load-balancing methods differ depending on the model of switch and software revision. Generally, load balancing is based on the contents of the Layer 2, 3, and/or 4 headers. If load balancing is based on only one header field in the frame, that single field is fed into the hashing function. If more than one header field is used, first, an XOR operation between the selected fields is used and only the result of this XOR is fed into the hashing function. The details of hashing functions in use are not public and can vary between different switch platforms. 

For the best balancing effect, the header fields on which balancing is based need to vary among the mix of frames sent over the Port-channel. For example, for a Layer 2 Portchannel connected to an access layer switch, most of the traffic going from the access layer switch to the distribution layer switch is probably going from clients to the default router. So most of the frames have different source MAC addresses but the same destination MAC address. For packets coming back from a distribution switch toward the access layer switch, many of the frames might have a source address of that same router, with differing destination MAC addresses. So, you could balance based on source MAC at the access layer switch and based on destination MAC at the distribution layer switch—or balance based on both fields on both switches. The goal is simply to use a balancing method for which the fields in the frames vary. 

The **port-channel load-balance** _type_ global level command sets the type of load balancing. The _type_ options include using source and destination MAC, IP addresses, and TCP and UDP ports—either a single field or both the source and destination. Because this command is global, it influences the operation of all EtherChannel bundles on a switch. Devices on opposite ends of an EtherChannel bundle can, and often do, use different load-balancing algorithms. 

The maximum number of active member links in an EtherChannel bundle is eight. This limit is reasonable, considering that Ethernet variants differ in speed by orders of tens (10 Mbps, 100 Mbps, 1 Gbps, 10 Gbps, 100 Gbps). More than eight links in an EtherChannel bundle is simply closing in on the next faster Ethernet variant, so it is reasonable to consider using a faster Ethernet variant in such cases instead. On many Catalyst switch platforms, the hashing function therefore produces a 3-bit result in the range of 0–7 whose values are assigned to the individual member links. With eight physical links in a bundle, 

156  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

each link is assigned exactly one value from this range. If there are fewer physical links, some of the links will be assigned multiple values from this range, and as a result, some of the links will carry more traffic than the others.  Table  3-7 describes the traffic amount ratios (P _n_ denotes the _n_ th port in a bundle). 

**Table 3-7** _Load Spread Ratios with Different Port Numbers in EtherChannel_ 

|**Table 3-7** _Load Spre_|_ad Ratios with Different Port Numbers in_|
|---|---|
|**Number of Ports in**|**Load-Balancing Ratios**|
|**the EtherChannel**||
|8|P1:P2:P3:P4:P5:P6:P7:P8→1:1:1:1:1:1:1:1|
|7|P1:P2:P3:P4:P5:P6:P7:P1→2:1:1:1:1:1:1|
|6|P1:P2:P3:P4:P5:P6:P1:P2→2:2:1:1:1:1|
|5|P1:P2:P3:P4:P5:P1:P2:P3→2:2:2:1:1|
|4|P1:P2:P3:P4:P1:P2:P3:P4→2:2:2:2|
|3|P1:P2:P3:P1:P2:P3:P1:P2→3:3:2|
|2|P1:P2:P1:P2:P1:P2:P1:P2→4:4|



Under ideal conditions, the traffic distribution across member links will be equal only if the number of links is eight, four, or two. With the eight resulting values from a 3-bit hash function, each value represents 1/8=12.5% of the traffic. The spread of the traffic by multiples of 12.5% is quite coarse. The indicated ratios can also be computed by using DIV and MOD operations: For example, with three links in a bundle, each link will be assigned 8 DIV 3 = 2 resulting hash values, plus 8 MOD 3 = 2 links will be handling an additional hash result value, yielding a ratio of (2+1):(2+1):2 = 3:3:2, or 37.5% : 37.5% : 25%. 

On other Cisco switch platforms, an 8-bit hash result is used although the EtherChannel is still limited to a maximum of eight links. Because the hash value allows for 256 possible results, each value represents a mere 1/256 = 0.390625% of the traffic. The spread of the traffic across links in a bundle is thus much more fine-grained. With three links, each of them would be assigned 256 DIV 3 = 85 resulting hash values, plus a 256 MOD 3 = 1 link would be handling an additional hash result value. So the traffic split ratio would be 86:85:85, or approximately 33.6% : 33.2% : 33.2%, much more balanced than 3:2:2. 

It is sometimes incorrectly stated that a Port-channel can only operate with two, four, or eight links. That is incorrect—a Port-channel can operate with any number of links between one and eight, inclusive. The spreading of total traffic across links can be uneven, however, if the number of links is not a power of 2, as previously explained. 

Chapter 3: Spanning Tree Protocol  157

## **Port-Channel Discovery and Configuration** 

When you are adding multiple ports to a particular Port-channel _on a single switch_ , several configuration items must be identical, as follows: 

**Key Topic** 

- Same speed and duplex settings. 

- Same operating mode (trunk, access, dynamic). 

- If not trunking, same access VLAN. 

- If trunking, same trunk type, allowed VLANs, and native VLAN. 

- On a single switch, each port in a Port-channel must have the same STP cost per VLAN on all links in the Port-channel. 

- No ports can have SPAN configured. 

Some of these limitations can change over time—it is recommended to consult the Configuration Guide for your particular switch platform and IOS version to stay up to date. 

When a new Port-channel is created, an **interface Port-channel** is automatically added to the configuration. This interface inherits the configuration of the first physical interface added to the Port-channel, and the configuration of all other physical interfaces added to the same Port-channel will be compared to the **interface Port-channel** configuration. If they differ, the physical interface will be considered as _suspended_ from the Port-channel, and it will not become a working member until its configuration is made identical to that of the Port-channel interface. Configuration changes performed on the **interface Portchannel** apply only to nonsuspended member ports; that is, commands applied to the Port-channel interface are pushed down only to those physical member ports whose configuration matched the **interface Port-channel** configuration before making the change. Therefore, reentering the configuration on the Port-channel interface in hopes of unifying the configuration of all member ports will not have an effect on those ports whose current configuration differs from that of the Port-channel interface. It is therefore recommended to adhere to the following guidelines when configuring Port-channels: 

**Key Topic** 

- Do not create the interface Port-channel manually before bundling the physical ports under it. Let the switch create it and populate its configuration automatically. 

- On the other hand, when removing a Port-channel, make sure to manually remove the **interface Port-channel** from the running config so that its configuration does not cause issues when a Port-channel with the same number is re-created later. 

- Be sure to make the configuration of physical ports identical before adding them to the same Port-channel. 

- If a physical port’s configuration differs from the **interface Port-channel** configuration, correct the physical port’s configuration first. Only then proceed to perform changes to the Port-channel interface configuration. 

158  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

- A Port-channel interface can either be Layer 2 (switched) or Layer 3 (routed), depending on whether the physical bundled ports are configured as Layer 2 ( **switchport** ) or Layer 3 ( **no switchport** ). After a Port-channel has been created with a particular operating level, it is not possible to change it to the other mode without re-creating it. If it is necessary to change between Layer 2 and Layer 3 levels of operation, the Port-channel must be removed from configuration and re-created after the physical ports are reconfigured for the required level of operation. It is possible, though, to combine the Layer 2 Port-channel on one switch with the Layer 3 Portchannel on another, although not necessarily a best practice. 

- Whenever resolving an issue with err-disabled ports under a Port-channel interface, be sure to shut down both the physical interfaces and the **interface Port-channel** itself. Only then try to reactivate them. If the problem persists, it is recommended to remove the Port-channel altogether from the configuration, unbundling the ports as a result, and re-create the Port-channel. 

You can statically configure interfaces to be in a Port-channel by using the **channelgroup** _number_ **mode on** interface subcommand. You would simply put the same command under each of the physical interfaces inside the Port-channel, using the same Portchannel number. This configuration forces the ports to become members of the same Port-channel without negotiating with the neighboring switch. This way of creating a Port-channel is strongly discouraged, though. If one switch considers multiple physical ports to be bundled under a single Port-channel while the neighboring switch still treats them as individual or assigns them into several bundles, permanent switching loops can occur. Also, this static Port-channel configuration is not capable of detecting whether the bundled ports are all connected to the same neighboring device. Having individual ports in a single Port-channel connect to different neighboring switches can again lead to permanent switching loops. To understand how the switch loop ensues, consider the topology shown in  Figure  3-16 . 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0199-04.png)


**----- Start of picture text -----**<br>
Designated Root<br>Port Port<br>Root Sec. Root<br>Designated Designated<br>Port Port<br>Alternate<br>Root Port<br>Port Designated<br>Port<br>AccessSw<br>**----- End of picture text -----**<br>


**Figure 3-16** _Permanent Switching Loop in a Misconfigured EtherChannel_ 

In this topology, the ports on the Secondary Root switch toward AccessSw have already been bundled in a Port-channel using **mode on** , and the switch uses them as a single EtherChannel right away, without negotiating with AccessSw. However, AccessSw is not yet configured for Port-channel on these ports, and treats them as individual links. 

Chapter 3: Spanning Tree Protocol  159 

**Key Topic** 

Because Port-channel interfaces are treated as single ports by STP, only a single BPDU is sent for the entire Port-channel interface, regardless of how many physical links are bundled. This BPDU is also subject to the hashing function and forwarded over a single link in the entire Port-channel bundle. Assuming that the Secondary Root has the second-lowest priority in this network and that the BPDUs are forwarded over the left link toward AccessSw, the corresponding port on AccessSw is Alternate Discarding. However, the AccessSw port on the right link is not receiving any BPDUs and becomes Designated Forwarding as a result. Even though such a port sends BPDUs, they will be ignored by the Secondary Root switch because they are inferior to its own BPDUs. Hence, a permanent switching loop is created. This is also the reason why a switch shuts down all physical ports when **no interface Port-channel** is issued—to prevent switching loops when Port-channel configuration is being removed. 

Note that if using RSTP/MST, the Dispute mechanism would detect this problem and put the Port-channel on the Secondary Root switch to the Discarding state, preventing this loop. In addition, Cisco has implemented yet another prevention mechanism called STP _EtherChannel Misconfig Guard_ on its switches. This mechanism makes an assumption that if multiple ports are correctly bundled into a Port-channel at the neighbor side, all BPDUs received over links in this Port-channel must have the same source MAC address in their Ethernet header, as the Port-channel interface inherits the MAC address of one of its physical member ports. If BPDUs sourced from different MAC addresses are received on a Port-channel interface, it is an indication that the neighbor is still treating the links as individual, and the entire Port-channel will be err-disabled. Note that the detection abilities of the EtherChannel Misconfig Guard are limited. In the topology in  Figure  3-16 , this mechanism will not help because the Secondary Switch receives just a single BPDU from AccessSw over the right link, and has no other BPDU to compare the source MAC address to. The mechanism would be able to detect a problem if, for example, there were three or more links between Secondary Root and AccessSw, or if the two existing links were bundled at the AccessSw instead of Secondary Root. The EtherChannel Misconfig Guard is active by default and can be deactivated using the **no spanning-tree etherchannel guard misconfig** global configuration command. 

It is therefore strongly recommended to use a dynamic negotiation protocol to allow switches to negotiate the creation of a Port-channel and verify whether the links are eligible for bundling. Those protocols are the Cisco-proprietary _Port Aggregation Protocol (PAgP)_ and the open IEEE 802.1AX (formerly 802.3ad) _Link Aggregation Control Protocol (LACP)_ . Both protocols offer relatively similar features though they are mutually incompatible. On a common Port-channel, both switches must use the same negotiation protocol; different Port-channel interfaces can use different negotiation protocols. Using LACP is generally preferred because of its open nature and widespread support. 

PAgP allows a maximum of eight links in a Port-channel. A switch will refuse to add more than eight links to a PAgP Port-channel. On current Catalyst switches, PAgP has no user-configurable parameters apart from the frequency of sending PAgP messages. This frequency is configurable on a per-port basis using the **pagp timer** { **normal | fast** } command; **normal** frequency is 30 seconds after the Port-channel is established, and **fast** is a 

160  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

1-second frequency. Other available commands related to PAgP have no effect on the forwarding behavior of the switch, and are kept only for backward compatibility with very old switches. 

With LACP, a maximum of 16 links can be placed into a Port-channel. Out of these links, at most eight links will be active members of the Port-channel. Remaining links will be put into a so-called Standby (sometimes also called Hot-Standby) mode. If an active link fails, one of the Standby links will be used to replace it. A single switch is in charge of selecting which Standby link will be promoted to the active state—it is the switch with the lower LACP System ID that consists of a configurable priority and the switch MAC address (the same concept as in STP). If there are multiple Standby links, the switch in control will choose the link with the lowest Port ID that again consists of a configurable priority and the port number. LACP priority of a switch can be globally configured using the **lacp system-priority** command, and the priority of a port can be set up using the **lacp port-priority** command. Both priorities can be configured in the range of 0–65535. 

To dynamically form a Port-channel using PAgP, you still use the **channel-group** command, with a mode of **auto** or **desirable** . To use LACP to dynamically create a Portchannel, use a mode of **active** or **passive** .  Table  3-8 lists and describes the modes and their meanings. 

**Table 3-8** _PAgP and LACP Configuration Settings and Recommendations_ 

||**Table 3-8** _PAgP_|_and LACP Configuration_|_Settings and Recommendations_|
|---|---|---|---|
|**Key**||||
|**Topic**|**PAgP Setting**|**LACP 802.1AX Setting**|**Action**|
||**auto**|**passive**|Uses PAgP or LACP, but waits on the other|
||||side to send the first PAgP or LACP message|
||**desirable**|**active**|Uses PAgP or LACP and initiates the|
||||negotiation|



**Note** Using **auto** (PAgP) or **passive** (LACP) on both switches prevents a Port-channel from forming dynamically. Cisco recommends the use of **desirable** mode (PAgP) or **active** mode (LACP) on ports that you intend to be part of a Port-channel on both devices. 

As remembering the mode keywords and the protocol they refer to ( **desirable** / **auto** for PAgP; **active** / **passive** for LACP) can be awkward, Cisco implemented the helper command **channel-protocol** { **pagp | lacp** } that can be used on physical interfaces to limit the accepted mode keywords to the stated negotiation protocol. In other words, entering **channel-protocol pagp** will allow the subsequent use of **desirable** or **auto** modes only; the **active** , **passive** , and **on** modes will be rejected. Similarly, using **channel-protocol lacp** will only permit the subsequent use of **active** or **passive** modes; the **desirable** , **auto** , and **on** modes will be rejected. 

Chapter 3: Spanning Tree Protocol  161 

**Note** A common misunderstanding is that the **channel-protocol** command can be used in combination with the **on** mode to start a particular negotiation protocol. This is incorrect. The **channel-protocol** command only causes the CLI to refuse any mode keywords that do not imply running the chosen negotiation protocol. 

When PAgP or LACP negotiate to form a Port-channel, the messages include the exchange of key information that allows detecting whether all links to be bundled under a single Port-channel are connected to the same neighbor and whether the neighbor is also willing to bundle them under a single Port-channel. These values include system IDs of both interconnected devices, identifiers of physical ports, and aggregation groups these ports fall under. It is sometimes believed that PAgP and LACP carry detailed information about individual port settings; that is incorrect. While PAgP and LACP make sure that the links to be bundled are all connected to the same neighboring switch and that both switches are willing to bundle them into a common Port-channel, they are neither capable nor supposed to verify whether ports on opposite sides of bundled links are otherwise identically configured. 

**Note** PAgP and LACP verify only whether the links to be bundled are consistently connected to the same neighboring device and are to be bundled into the same link aggregation group. However, neither of these protocols performs checks on whether the ports on this switch and its neighbor are configured identically with respect to their operating mode, allowed VLANs, native VLAN, encapsulation, and so on. 

When PAgP or LACP completes the process, a new Port-channel interface exists and is used as if it were a single port for STP purposes, with balancing taking place based on the global load-balancing method configured on each switch.

## **Troubleshooting Complex Layer 2 Issues** 

Troubleshooting is one of the most challenging aspects of CCIE study. The truth is, we can’t teach you to troubleshoot in the pages of a book; only time and experience bring strong troubleshooting skills. We can, however, provide you with two things that are indispensable in learning to troubleshoot effectively and efficiently: process and tools. The focus of this section is to provide you with a set of Cisco IOS–based tools, beyond the more common ones that you already know, as well as some guidance on the troubleshooting process for Layer 2 issues that you might encounter. 

In the CCIE Routing and Switching lab exam, you will encounter an array of troubleshooting situations that require you to have mastered fast, efficient, and thorough troubleshooting skills. In the written exam, you’ll need a different set of skills—mainly, the knowledge of troubleshooting techniques that are specific to Cisco routers and switches, and the ability to interpret the output of various **show** commands and possibly debug output. You can also expect to be given an example along with a problem statement. You 

162  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

will need to quickly narrow the question down to possible solutions and then pinpoint the final solution. This requires a different set of skills than what the lab exam requires, but spending time on fundamentals as you prepare for the qualification exam will provide a good foundation for the lab exam environment. 

As in all CCIE exams, you should expect that the easiest or most direct ways to a solution might be unavailable to you. In troubleshooting, perhaps the easiest way to the source of most problems is through the **show run** command or variations on it. Therefore, we’ll institute a simple “no **show run** ” rule in this section that will force you to use your knowledge of more in-depth troubleshooting commands in the Cisco IOS portion of this section. 

In addition, you can expect that the issues you’ll face in this part of the written exam will need more than one command or step to isolate and resolve.

## **Layer 2 Troubleshooting Process** 

From the standpoint of troubleshooting techniques, two basic stack-based approaches come into play depending on what type of issue you’re facing. The first of these is the climb-the-stack (or bottom-up) approach, where you begin at Layer 1 and work your way up until you find the problem. Alternatively, you can start at Layer 7 and work your way down in a top-down approach; however, in the context of the CCIE Routing and Switching exams, the climb-the-stack approach generally makes more sense. 

Another approach is often referred to as the divide-and-conquer method. With this technique, you start in the middle of the stack (usually where you see the problem) and work your way down or up the stack from there until you find the problem. In the interest of time, which is paramount in an exam environment, the divide-and-conquer approach usually provides the best results. Because this section deals with Layer 2 issues, it starts at the bottom and works up. 

Some lower-level issues that might affect Layer 2 connectivity include the following:

## **Key Topic** 

- **Cabling:** Check the physical soundness of the cable as well as the use of a correctly pinned cable. If the switch does not support Automatic Medium-Dependent Interface Crossover (Auto-MDIX), the correct choice of either crossover or straightthrough cable must be made. On many Catalyst platforms (not all, though), configuring both speed and duplex statically on a port results in autonegotiation including Auto-MDIX to be deactivated on that port. That can lead both to duplex mismatches and to a link going down if the cable required the port to perform automatic crossover. 

- **Speed or duplex mismatch:** Most Cisco devices will correctly sense speed and duplex when both sides of the link are set to Auto, but a mismatch can cause the line protocol on the link to stay down. 

- **Device physical interface:** It is possible for a physical port to break. 

Chapter 3: Spanning Tree Protocol  163

## **Layer 2 Protocol Troubleshooting and Commands** 

In addition to the protocol-specific troubleshooting commands that you have learned so far, this section addresses commands that can help you isolate problems through a solid understanding of the information they present. We will use a variety of examples of command output to illustrate the key parameters you should understand.

## Troubleshooting Using Cisco Discovery Protocol 

Cisco Discovery Protocol (CDP) is a proprietary protocol that is used to help administrators collect information about neighboring Cisco devices. CDP makes it possible to gather hardware and protocol information about neighbor devices, which is useful information for troubleshooting or network discovery. 

CDP messages are generated every 60 seconds as Layer 2 multicast messages on each of a device’s active interfaces. The information shared in a CDP packet about a device includes, but is not limited to, the following: 

- Name of the device configured with the **hostname** command 

- IOS software version 

- Hardware capabilities, such as routing, switching, and/or bridging 

- Hardware platform, such as 2800, 2960, or 1900 

- The Layer 3 address(es) of the device 

- The interface that the CDP update was generated on 

- Duplex setting of the interface that CDP was generated on 

- VTP domain of the device if relevant 

- Native VLAN of the sending port if relevant 

CDP enables devices to share basic configuration information without even configuring any protocol-specific information and is enabled by default on all common interfaces (CDP might be deactivated on less typical interfaces such as Virtual-Template or multipoint Frame Relay). CDP is a Data Link Layer utility found in IOS that resides at Layer 2 of the OSI model; as such, CDP is not routable and can only operate over directly connected interfaces. As a general rule, CDP is active by default on devices. 

CDP updates are generated every 60 seconds with a hold-down period of 180 seconds for a missing neighbor. The **no cdp run** command globally disables CDP, while the **no cdp enable** command disables CDP on an interface. Disabling CDP globally and enabling it on individual interfaces is not possible. We can use the **show cdp neighbors** command to list any directly connected Cisco neighboring devices. Additionally, we can use the **detail** keyword to display detailed information about the neighbor, including its Layer 3 addressing. 

164  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Example  3-3 shows the CDP timer, which is how often CDP packets are sent, and the CDP holdtime, which is the amount of time that the device will hold packets from neighbor devices. 

**Example 3-3** _CDP Timers_ 

Router_2# **show cdp** Global CDP information: Sending CDP packets every 60 seconds Sending a holdtime value of 180 seconds 

Example  3-4 shows how we can use the following commands to set CDP timer and holdtime values to something other than the defaults. 

**Example 3-4** _Adjusting CDP Timers_ 

Router_2# **conf t** Enter configuration commands, one per line.  End with CNTL/Z. Router_2(config)# **cdp timer 90** Router_2(config)# **cdp holdtime 360** 

CDP can be disabled with the **no cdp run** command in global configuration mode. 

Because a device stores the CDP information in its runtime memory, you can view it with a **show** command. It will only show information about directly connected devices because CDP packets are not passed through Cisco devices.  Example  3-5 shows such output. 

**Example 3-5** _CDP Verification Commands_ 

Router_2# **show cdp neighbors** Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge S - Switch, H - Host, I - IGMP, r - Repeater Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID Router3             Ser 1          120           R        2500      Ser 0 Router1             Eth 1          180           R        2500      Eth 0 Switch1             Eth 0          240           S        1900      2 

! CDP Neighbor Information includes 

- ! Neighbor's device ID 

- ! Local port type and number 

- ! Holdtime value (in seconds) 

- ! Neighbor's network device capability 

- ! Neighbor's hardware platform 

- ! Neighbor's remote port type and number 

- ! In addition to this we can employ the **show cdp entry** _device-id_ 

- ! command to show  more information about a specified neighbor. 

Chapter 3: Spanning Tree Protocol  165 

Router_2# **show cdp entry Router1** ------------------------Device ID: Router1 Entry address(es): IP address: 192.168.1.2 Platform: cisco 2500, Capabilities: Router Interface: Ethernet1,  Port ID (outgoing port): Ethernet0 Holdtime : 180 sec Version: Cisco Internetwork Operating System Software IOS (tm) 2500 Software (2500-JS-L), Version 11.2(15) RELEASED SOFTWARE (fcl) Copyright (c) 1986-1998 by Cisco Systems, Inc. Compiled Mon 06-Jul-98 22:22 by tmullins 

! The following is a sample output for one neighbor from the **show cdp neighbors** ! **detail** command. Additional detail is shown about neighbors, including network ! address, enabled protocols, and software version. 

Router_2# **show cdp neighbors detail** Device ID: 008024 1EEB00 (milan-sw-1-cat9k) Entry address(es): IP address: 1.15.28.10 Platform: CAT5000, Capabilities: Switch Interface: Ethernet1/0, Port ID (outgoing port): 2/7 Holdtime : 162 sec Version : Cisco Catalyst 5000 Duplex Mode: full Native VLAN: 42 VTP Management Domain: 'Accounting Group'

## Troubleshooting Using Link Layer Discovery Protocol 

Where Cisco Discovery Protocol (CDP) is a device discovery protocol that runs over Layer 2 on all Cisco-manufactured devices (routers, bridges, access servers, and switches) that allows network management applications to automatically discover and learn about other Cisco devices connected to the network, we have to ask the question, “What happens if we have to work with non-Cisco equipment?” 

166  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

To support non-Cisco devices and to allow for interoperability between other devices, IOS also supports the IEEE 802.1AB Link Layer Discovery Protocol (LLDP). LLDP is a neighbor discovery protocol similar to CDP that is used for network devices to advertise information about themselves to other devices on the network. This protocol runs over the Data Link Layer, which allows two systems running different network layer protocols to learn about each other. 

LLDP supports a set of attributes that it uses to discover neighbor devices. These attributes contain type, length, and value descriptions and are referred to as TLVs. LLDPsupported devices can use TLVs to receive and send information to their neighbors. This protocol can advertise details such as configuration information, device capabilities, and device identity. 

The switch supports these basic management TLVs. These are mandatory LLDP TLVs: 

- Port description TLV 

- System name TLV 

- System description TLV 

- System capabilities TLV 

- Management address TLV 

Similar to CDP, configuration on a Cisco device can be made in the global or interface mode. 

Example  3-6 shows how to globally enable LLDP and to manipulate its configuration.

## **Example 3-6** _LLDP Configuration and Verification_ 

- ! This example shows how to enable LLDP. First, LLDP must be 

- ! activated globally. Then, instead of having a single 

! enable keyword similar to **cdp enable** , LLDP has **lldp transmit** and **lldp receive** ! commands. By default, they are both set, so a port automatically sends and ! receives LLDP messages. The following example shows the use of the commands. 

Switch# **configure terminal** Switch(config)# **lldp run** Switch(config)# **interface fa0/1** Switch(config-if)# **lldp transmit** Switch(config-if)# **lldp receive** Switch(config-if)# **end** 

- ! You can configure the frequency of LLDP updates, the amount of time to hold the 

- ! information before discarding it, and the initialization delay time. 

Chapter 3: Spanning Tree Protocol  167 

Switch# **configure terminal** Switch(config)# **lldp holdtime 120** Switch(config)# **lldp reinit 2** Switch(config)# **lldp timer 30** Switch(config)# **end**

## Troubleshooting Using Basic Interface Statistics 

The **show interfaces** command is a good place to start troubleshooting interface issues. It will tell you whether the interface has a physical connection and whether it was able to form a logical connection. The link duplex and bandwidth are shown, along with errors and collisions.  Example  3-7 shows output from this command, with important statistics highlighted. 

**Example 3-7** _Troubleshooting with the_ **show interface** _Command_ 

! Shows a physical and logical connection SW4# **show int fa0/21** FastEthernet0/21 is up, line protocol is up (connected) Hardware is Fast Ethernet, address is 001b.d4b3.8717 (bia 001b.d4b3.8717) MTU 1500 bytes, BW 100000 Kbit, DLY 100 usec, reliability 255/255, txload 1/255, rxload 1/255 Encapsulation ARPA, loopback not set Keep alive set (10 sec) 

! Negotiated or configured speed and duplex 

Full-duplex, 100Mb/s, media type is 10/100BaseTX input flow-control is off, output flow-control is unsupported ARP type: ARPA, ARP Timeout 04:00:00 Last input 00:00:01, output 00:00:08, output hang never Last clearing of "show interface" counters never Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0 Queueing strategy: fifo Output queue: 0/40 (size/max) 

5 minute input rate 0 bits/sec, 0 packets/sec 

5 minute output rate 0 bits/sec, 0 packets/sec 16206564 packets input, 1124307496 bytes, 0 no buffer Received 14953512 broadcasts (7428112 multicasts) 

! CRC errors, runts, frames, collisions or late collisions 

- ! may indicate a duplex mismatch 

- 0 runts, 0 giants, 0 throttles 

168  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored 

0 watchdog, 7428112 multicast, 0 pause input 

0 input packets with dribble condition detected 2296477 packets output, 228824856 bytes, 0 underruns 

- 0 output errors, 0 collisions, 1 interface resets 

- 0 babbles, 0 late collision, 0 deferred 

- 0 lost carrier, 0 no carrier, 0 PAUSE output 

0 output buffer failures, 0 output buffers swapped out 

If an interface shows as up/up, you know that a physical and logical connection has been made, and you can move on up the stack in troubleshooting. If it shows as up/ down, you have some Layer 2 troubleshooting to do. An interface status of err-disable could be caused by many different problems, some of which are discussed in this chapter. Common causes include a security violation or detection of a unidirectional link. Occasionally, a duplex mismatch will cause this state. 

Chapter 1,  “Ethernet Basics,” showed examples of a duplex mismatch, but the topic is important enough to include here. Duplex mismatch might be caused by hard-coding one side of the link to full duplex but leaving the other side to autonegotiate duplex. A 10/100 interface will default to half duplex if the other side is 10/100 and does not negotiate. It could also be caused by an incorrect manual configuration on both sides of the link. A duplex mismatch usually does not bring the link down; it just creates suboptimal performance by causing collisions. 

You would suspect a duplex mismatch if you saw collisions on a link that should be capable of full duplex, because a full-duplex link should by definition never have collisions. A link that is half duplex on both sides will show some interface errors. But more than about 1 percent to 2 percent of the total traffic is cause for a second look. Watch for the following types of errors: 

- **Runts:** Runts are frames smaller than 64 bytes. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0209-12.png)


**----- Start of picture text -----**<br>
Key<br>Topic<br>**----- End of picture text -----**<br>


- **CRC errors:** The frame’s cyclic redundancy checksum value does not match the one calculated by the switch or router. 

- **Frames:** Frame errors have a CRC error and contain a noninteger number of octets. 

- **Alignment:** Alignment errors have a CRC error and an odd number of octets. 

- **Collisions:** Look for collisions on a full-duplex interface (meaning that the interface operated in half-duplex mode at some point in the past), or excessive collisions on a half-duplex interface. 

- **Late collisions on a half-duplex interface:** A late collision occurs after the first 64 bytes of a frame. 

Chapter 3: Spanning Tree Protocol  169 

Another command to display helpful interface statistics is **show controllers** , shown in Example  3-8 . The very long output from this command is another place to find the number of frames with bad frame checks, CRC errors, collisions, and late collisions. In addition, it tells you the size breakdown of frames received and transmitted. A preponderance of one-size frames on an interface that is performing poorly can be a clue to the application sending the frames. Another useful source of information is the interface autonegotiation status and the speed/duplex capabilities of it and its neighbor, shown at the bottom of  Example 3-8 . 

**Example 3-8** _Troubleshooting with the_ **show controllers** _Command_ 

R1# **show controllers fastEthernet 0/0** Interface FastEthernet0/0 Hardware is MV96340 HWIDB: 46F92948, INSTANCE: 46F939F0, FASTSEND: 4374CB14, MCI_INDEX: 0 Aggregate MIB Counters ---------------------Rx Good Bytes: 27658728                      Rx Good Frames: 398637 Rx Bad Bytes: 0                              Rx Bad Frames: 0 Rx Broadcast Frames: 185810                  Rx Multicast Frames: 181353 Tx Good Bytes: 3869662                       Tx Good Frames: 36667 Tx Broadcast Frames: 0                       Tx Multicast Frames: 5684 Rx+Tx Min-64B Frames: 412313                 Rx+Tx 65-127B Frames: 12658 Rx+Tx 128-255B Frames: 0                     Rx+Tx 256-511B Frames: 10333 Rx+Tx 512-1023B Frames: 0                    Rx+Tx 1024-MaxB Frames: 0 Rx Unrecog MAC Ctrl Frames: 0 Rx Good FC Frames: 0                         Rx Bad FC Frames: 0 Rx Undersize Frames: 0                       Rx Fragment Frames: 0 Rx Oversize Frames: 0                        Rx Jabber Frames: 0 Rx MAC Errors: 0                             Rx Bad CRCs: 0 Tx Collisions: 0                             Tx Late Collisions: 0 ! [output omitted] AUTONEG_EN PHY Status (0x01): AUTONEG_DONE LINK_UP Auto-Negotiation Advertisement (0x04): 100FD 100HD 10FD 10HD Link Partner Ability (0x05): 100FD 100HD 10FD 10HD ! output omitted 

170  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Troubleshooting Spanning Tree Protocol** 

Spanning-tree issues are possible in a network that has not been properly configured. Previous sections of this chapter discussed ways to secure STP. One common STP problem is a change in the root bridge. If the root bridge is not deterministically configured, a change in the root can affect network connectivity. To lessen the chance of this, use Rapid STP and all the tools necessary to secure the root and user ports.  Example  3-1 showed commands to check the root bridge and other STP parameters, including the following: 

**show spanning-tree** [ **vlan** _number_ ] **root** [ **detail** | **priority** [ **system-id** ] ] 

Keep in mind that when BPDU Guard is enabled, a port is error-disabled if it receives a BPDU. You can check this with the **show interfaces status err-disabled** command. In addition, switching loops can result if the **spanning-tree portfast trunk** command is enabled on a trunk port toward another switch, or an interface has a duplex mismatch. One symptom of a loop is flapping MAC addresses. A port protected by Root Guard is put in a root-inconsistent state if it tries to become a Root Port: a Root and Alternate Port with Loop Guard configured is put in a loop-inconsistent state if it stops receiving BPDUs. You can check this with the **show spanning-tree inconsistent ports** command. Whether an interface is error-disabled or put into an inconsistent state, the port is effectively shut down to user traffic. 

Cisco STP implementation recognizes many kinds of port inconsistencies.  Table  3-9 summarizes them and the reasons causing them. 

**Table 3-9** _Types of STP Inconsistencies and Their Causes_ 

|**Key**<br>**Topic**||
|---|---|
||**Inconsistency Type**<br>**Description and Probable Cause of Inconsistency**|
||Type<br>(*TYPE_Inc)<br>PVST+ BPDUs are received on a non-802.1Q port. Usually caused<br>by interconnecting access and trunk ports.|
||Port VLAN ID<br>(*PVID_Inc)<br>PVST+ BPDUs are received in a different VLAN than they were<br>originated in. Usually caused by native VLAN mismatch on a trunk.|
||PVST Simulation<br>(*PVST_Inc)<br>PVST+ BPDUs received on an MST boundary port do not meet the<br>PVST Simulation consistency criteria.|
||Loop<br>(*LOOP_Inc)<br>A Root or Alternate Port tried to become Designated after BPDUs<br>stopped arriving. Seen only on Loop Guard–protected ports.|
||Root<br>(*ROOT_Inc)<br>A port tried to become a Root Port after receiving superior BPDUs.<br>Seen only on Root Guard-protected ports. Also, on older switches,<br>this state was displayed in place of the PVST_Inc state if PVST<br>Simulation Inconsistency was encountered on a port.|
||Bridge Assurance<br>(*BA_Inc)<br>A port stopped receiving BPDUs. Seen only on Bridge Assurance–<br>protected ports.|



Chapter 3: Spanning Tree Protocol  171

## Troubleshooting Trunking 

Trunks that fail to form can result from several causes. With an 802.1Q trunk, a native VLAN mismatch is usually the first thing troubleshooters look at. You should additionally check the Dynamic Trunking Protocol (DTP) negotiation mode of each side of the trunk.  Table  2-9 in  Chapter  2 , “Virtual LANs and VLAN Trunking,” lists the combinations of DTP configurations that will lead to successful trunking. 

A VLAN Trunking Protocol (VTP) domain mismatch has been known to prevent trunk formation, even in switches that are in VTP Transparent mode, because the VTP domain name is carried in DTP messages. The switch’s logging output will help you greatly. This is shown in  Example  3-9 , along with some commands that will help you troubleshoot trunking problems. In  Example  3-9 , two switches are configured with 802.1Q native VLANs 10 and 99, and DTP mode desirable. Both are VTP transparent and have different VTP domain names. Some output irrelevant to the example is omitted. 

**Example 3-9** _Troubleshooting Trunking_ 

! These errors messages were logged by the switch 

%CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on FastEthernet1/0/21 (10), with sw4 FastEthernet0/21 (99) %SPANTREE-2-RECV_PVID_ERR: Received BPDU with inconsistent peer vlan id 99 on FastEthernet1/0/21 VLAN10 %DTP-5-DOMAINMISMATCH: Unable to perform trunk negotiation on port Fa1/0/21 because of VTP domain mismatch. ! This command shows that the port is configured to trunk ! (Administrative Mode) but is not performing as a trunk ! (Operational Mode) SW2# **show int fa 1/0/1 switchport** Name: Fa1/0/1 Switchport: Enabled Administrative Mode: dynamic desirable Operational Mode: static access Administrative Trunking Encapsulation: negotiate Operational Trunking Encapsulation: native Negotiation of Trunking: On Access Mode VLAN: 1 (default) Trunking Native Mode VLAN: 10 (NATIVE_10) Administrative Native VLAN tagging: enabled ! output omitted 

! Trunking VLANs Enabled: 3,99 

! The port is shown as inconsistent due to native VLAN mismatch 

172  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

SW4# **show spanning-tree inconsistentports** Name         Interface                Inconsistency ------------ ------------------------ -----------------VLAN0099     FastEthernet0/21         Port VLAN ID Mismatch Number of inconsistent ports (segments) in the system : 1 

! Once the errors are corrected, the interface shows as a trunk 

SW4# **show interfaces trunk** Port        Mode         Encapsulation  Status      Native vlan Fa0/21      desirable    802.1q         trunking    99 ! Output omitted 

If your trunks are connected and operating, but user connectivity is not working, check the VLANs allowed on each trunk. Make sure that the allowed VLANs match on each side of the trunk, and that the users’ VLAN is on the allowed list (assuming that it should be). Either look at the interface configuration or use the **show interfaces trunk** and **show interfaces switchport** commands shown in  Example  3-9 to find that information.

## Troubleshooting VTP 

If you choose to use anything other than VTP Transparent mode in your network, you should be aware of the ways to break it. VTP will fail to negotiate a neighbor status if the following items do not match: 

- VTP version 

- VTP domain 

- VTP password 

In addition, recall that VTP runs over trunk links only, so you must have an operational trunk before expecting VTP to act. To prevent your VLAN database from being altered when adding a VTPv1 or VTPv2 switch to the VTP domain, follow these steps: 

- **Step 1.** Change the VTP mode to Transparent, which will reset the configuration revision number to 0. 

- **Step 2.** Configure the remaining appropriate VTP parameters. 

- **Step 3.** Configure trunking. 

- **Step 4.** Connect the switch to the network. 

VTPv3 prevents a switch, even with a higher revision number, from asserting its database over other switches if its idea of who is the primary server differs from that of its neighbors. 

The first part of  Example  3-10 shows a VTP client with a password that doesn’t match its neighbor (note the error message). The switch does not show an IP address in the last 

Chapter 3: Spanning Tree Protocol  173 

line because it has not been able to negotiate a VTP relationship with its neighbor. In the second part of the example, the configuration has been corrected. Now the neighbor’s IP address is listed as the VTP updater. 

**Example 3-10** _Troubleshooting VTP_ 

! Wrong password is configured SW4# **show vtp status** VTP Version                     : running VTP1 (VTP2 capable) Configuration Revision          : 0 Maximum VLANs supported locally : 1005 Number of existing VLANs        : 5 VTP Operating Mode              : Client VTP Domain Name                 : CCIE VTP Pruning Mode                : Disabled VTP V2 Mode                     : Disabled VTP Traps Generation            : Disabled MD5 digest                      : 0xA1 0x7C 0xE8 0x7E 0x4C 0xF5 0xE3 0xC8 *** MD5 digest checksum mismatch on trunk: Fa0/23 *** *** MD5 digest checksum mismatch on trunk: Fa0/24 *** Configuration last modified by 0.0.0.0 at 7-24-09 03:12:27 

! On some IOS versions, a message about MD5 digest failing is not displayed. 

! In these cases, using **debug sw-vlan vtp events** may be helpful - look for output ! similar to this: 

*Jul 24 11:01:42.558: VTP LOG RUNTIME: MD5 digest failing calculated = D7 17 28 01 4E 1D E6 65 67 0A 9D 73 71 EA 5A 5C transmitted = C2 93 A7 15 E5 0C 0B 9D DD 24 BB ED 18 4C 97 45 

! Command output after the misconfiguration was corrected 

SW4# **show vtp status** VTP Version                     : running VTP2 Configuration Revision          : 5 Maximum VLANs supported locally : 1005 Number of existing VLANs        : 9 VTP Operating Mode              : Client VTP Domain Name                 : CCIE VTP Pruning Mode                : Disabled VTP V2 Mode                     : Enabled VTP Traps Generation            : Disabled MD5 digest                      : 0xDD 0x6C 0x64 0xF5 0xD2 0xFE 0x9B 0x62 Configuration last modified by 192.168.250.254 at 7-24-09 11:02:43 

174  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## Troubleshooting EtherChannels 

Table  3-8 listed the LACP and PAgP settings. If your EtherChannel is not coming up, check these settings. If you are using LACP, at least one side of each link must be set to **active** . If you are using PAgP, at least one side of the link must be set to **desirable** . If you are not using a channel negotiation protocol, make sure that both sides of the links are set to **on** . 

Remember that the following rules apply to all ports within an EtherChannel: 

- Speed and duplex must match. 

- Interface type—access, trunk, or routed—must match. 

- Trunk configuration—encapsulation, allowed VLANs, native VLAN, and DTP mode—must match. 

- If a Layer 2 EtherChannel is not a trunk, all ports must be assigned to the same VLAN. 

- No port in the EtherChannel can be a Switched Port Analyzer (SPAN) port. 

- On a Layer 3 EtherChannel, the IP address must be on the Port-channel interface, not a physical interface. 

To troubleshoot an EtherChannel problem, check all the parameters in the preceding list. Example  3-11 shows some commands to verify the logical and physical port configuration for an EtherChannel. QoS configuration must match and must be configured on the physical ports, not the logical one. 

**Example 3-11** _Troubleshooting EtherChannels_ 

! The **show etherchannel summary** command gives an overview of the ! channels configured, whether they are Layer 2 or Layer 3, the ! interfaces assigned to each, and the protocol used if any L3SW4# **show etherchannel summary** Flags:  D - down        P - bundled in port-channel I - stand-alone s - suspended H - Hot-standby (LACP only) R - Layer3      S - Layer2 U - in use      f - failed to allocate aggregator M - not in use, minimum links not met u - unsuitable for bundling w - waiting to be aggregated d - default port Number of channel-groups in use: 3 

Chapter 3: Spanning Tree Protocol  175 

Number of aggregators:           3 Group  Port-channel  Protocol  Ports ------+-------------+---------+------------------------------------------14     Po14(SU)      LACP    Fa0/3(P) 24     Po24(RU)       -      Fa0/7(P)  Fa0/8(P)  Fa0/9(P)  Fa0/10(P) 34     Po34(RU)      PAgP    Fa0/1(P)  Fa0/2(P) ! The **show interface etherchannel** command lets you verify that the ! interface is configured with the right channel group and ! protocol settings L3SW3# **show int fa0/1 etherchannel** Port state    = Up  Mstr In-Bndl Channel group = 34      Mode = On     Gcchange = - Port-channel  = Po34    GC   =   -    Pseudo port-channel = Po34 Port index    = 0       Load = 0x00   Protocol =  PAgP Age of the port in the current state: 1d:07h:28m:19s 

! The **show interface portchannel** command produces output similar 

! to a physical interface. It allows you to verify the ports 

! assigned to the channel and the type of QoS used 

L3SW3# **show int port-channel 23** Port-channel23 is up, line protocol is up (connected) Hardware is EtherChannel, address is 001f.2721.8643 (bia 001f.2721.8643) Internet address is 10.1.253.13/30 MTU 1500 bytes, BW 200000 Kbit, DLY 100 usec, reliability 255/255, txload 1/255, rxload 1/255 Encapsulation ARPA, loopback not set Keepalive set (10 sec) Full-duplex, 100Mb/s, link type is auto, media type is unknown input flow-control is off, output flow-control is unsupported Members in this channel: Fa0/3 Fa0/4 ARP type: ARPA, ARP Timeout 04:00:00 Last input 00:00:02, output 00:00:00, output hang never Last clearing of "show interface" counters never Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0 Queueing strategy: fifo

## **Approaches to Resolving Layer 2 Issues** 

Table  3-10 presents some generalized types of Layer 2 issues and ways of approaching them, including the relevant Cisco IOS commands. 

176  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 3-10** _Layer 2 Troubleshooting Approach and Commands_ 

|**Problem**|**Approach**|**Helpful IOS Commands**|
|---|---|---|
|Lack of reachability|Eliminate Layer 1 issues with|**show interface**|
|to devices in the same<br>VLAN|**show interface **commands.<br>Verify that the VLAN exists<br>on the switch.|**show vlan**<br> **show interface switchport**|
||Verify that the interface<br>is assigned to the correct|**traceroute mac ** _source-mac_<br>_destination-mac_|
||VLAN.|**show interface trunk**|
||Verify that the VLAN is||
||allowed on the trunk.||
|Intermittent reachability|Check for excessive interface|**show interface**|
|to devices in the same<br>VLAN|traffic.<br>Check for unidirectional<br>links.|**show spanning-tree**<br> **show spanning-tree root**|
||Check for spanning-tree|**show mac address-table**|
||problems such as BPDU||
||floods or flapping MAC||
||addresses.||
|No connectivity between|Check for interfaces that are|**show interfaces status err-**|
|switches|shut down.|**disabled**|
||Verify that trunk links and|**show interfaces trunk**|
||EtherChannels are active.|**show etherchannel summary**|
||Verify that BPDU Guard<br>is not enabled on a trunk|**show spanning-tree detail**|
||interface.||
|Poor performance across|Check for a duplex|**show interface**|
|a link|mismatch.||



In summary, when troubleshooting Layer 2 issues, check for interface physical problems or configuration mismatches. Verify that STP is working as expected. If you are using VTP, make sure that it is configured properly on each switch. For trunking problems, check native VLAN and DTP configuration. When troubleshooting port channels, verify that the interface parameters are the same on both sides. 

Chapter 3: Spanning Tree Protocol  177

## **Foundation Summary** 

This section lists additional details and facts to round out the coverage of the topics in this chapter. Unlike most of the Cisco Press Exam Certification Guides, this “Foundation Summary” does not repeat information presented in the “Foundation Topics” section of the chapter. Please take the time to read and study the details in the “Foundation Topics” section of the chapter, as well as review items noted with a Key Topic icon. 

Table  3-11 lists the protocols mentioned in this chapter and their respective standards documents. 

**Table 3-11** _Protocols and Standards for  Chapter  3_ 

|**Table 3-11** _Pro_|_tocols and Standards for  Chapter_|
|---|---|
|**Name**|**Standards Body**|
|RSTP|IEEE 802.1D (formerly 802.1w)|
|MST|IEEE 802.1Q (formerly 802.1s)|
|STP|Formerly IEEE 802.1D|
|LACP|IEEE 802.1AX (formerly 802.3AD)|
|Dot1Q trunking|IEEE 802.1Q|
|PVST+|Cisco|
|RPVST+|Cisco|
|PAgP|Cisco|



Table  3-12 lists the three key timers that impact STP convergence. 

**Table 3-12** _IEEE 802.1D STP Timers_ 

|**Timer**|**Default**|**Purpose**|
|---|---|---|
|Hello|2 sec|Interval at which the root sends Configuration BPDUs|
|Forward Delay|15 sec|Time that switch leaves a port in the Listening state and the|
|||Learning state; also used as the short CAM timeout timer|
|MaxAge|20 sec|Time without hearing a Hello before expiring the stored BPDU|



Table  3-13 lists some of the key IOS commands related to the topics in this chapter. The command syntax for switch commands was taken from the _Catalyst 3560 Switch Command Reference, 15.0(2)SE_ . 

178  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

**Table 3-13** _Command Reference for  Chapter  3_ 

|**Command**|**Description**|
|---|---|
|**spanning-tree mode **{**mst **|**pvst **||Global config command that sets the STP mode.|
|**rapid-pvst**}||
|[**no**]**spanning-tree vlan ** _vlan-id_|Enables or disables STP inside a particular VLAN|
||when using PVST+ or RPVST+ .|
|**spanning-tree vlan ** _vlan-id_{**forward-**|Global config command to set a variety of STP|
|**time ** _seconds_|**hello-time ** _seconds_|**max-**|parameters when using PVST+ or RPVST+.|
|**age ** _seconds_|**priority ** _priority_| {**root**||
|{**primary **|**secondary**} [**diameter ** _net-_||
|_diameter_[**hello-time ** _seconds_]]}}||
|**spanning-tree [ vlan ** _x_|**mst ** _x_]**cost ** _y_|Interface subcommand used to set interface|
||costs, per VLAN. If the**vlan **or**mst **keyword|
||is omitted, applies to all unspecified VLANs or|
||MST instances.|
|**spanning-tree [ vlan ** _x_|**mst ** _x_]**port-**|Interface subcommand used to set port priority,|
|**priority ** _y_|per VLAN. If the**vlan **or**mst **keyword is|
||omitted, applies to all unspecified VLANs or|
||MST instances.|
|**channel-group ** _channel-group-number_|Interface subcommand that places the interface|
|**mode **{**auto **[**non-silent**] |**desirable**|into a Port-channel, and sets the negotiation|
|[**non-silent**] |**on **|**active **|**passive**}|parameters.|
|**channel-protocol **{**lacp **|**pagp**}|Interface subcommand to define which|
||protocol to allow to configure for EtherChannel|
||negotiation.|
|**interface port-channel ** _port_-_channel-_|Global command that allows entering the logical|
|_number_|interface representing the Port-channel bundle.|
|**spanning-tree portfast **[**trunk **]|Interface subcommand that enables PortFast on|
||the interface.|
|**spanning-tree bpduguard {enable |**|Interface command that enables or disables|
|**disable}**|BPDU Guard on the interface.|
|**spanning-tree mst ** _instance-id_ **priority**|Global command used to set the priority of an|
|_priority_|MST instance.|
|**spanning-tree mst configuration**|Global command that puts the user in MST|
||configuration mode.|
|**show spanning-tree bridge | root | brief**|EXEC command to show various details about|
|**| summary**|STP operation.|
|**show interfaces**|Displays Layer 1 and 2 information about an|
||interface.|
|**show interfaces trunk**|Displays the interface trunk configuration.|
|**show etherchannel [summary]**|Lists EtherChannels configured and their status.|



Chapter 3: Spanning Tree Protocol  179 

|**Command**|**Description**|
|---|---|
|**show interfaces switchport**|Displays the interface trunking and VLAN|
||configuration.|
|**show vtp status**|Displays the VTP configuration.|
|**show controllers**|Displays physical interface characteristics as well|
||as traffic and error types.|

## **Memory Builders** 

The CCIE Routing and Switching written exam, like all Cisco CCIE written exams, covers a fairly broad set of topics. This section provides some basic tools to help you exercise your memory about some of the broader topics covered in this chapter.

## **Fill in Key Tables from Memory** 

Appendix  E , “Key Tables for CCIE Study,” on the CD in the back of this book, contains empty sets of some of the key summary tables in each chapter. Print  Appendix  E , refer to this chapter’s tables in it, and fill in the tables from memory. Refer to  Appendix  F , “Solutions for Key Tables for CCIE Study,” on the CD to check your answers.

## **Definitions** 

Next, take a few moments to write down the definitions for the following terms: 

CST, CIST, STP, MST, RSTP, Hello timer, MaxAge timer, ForwardDelay timer, Blocking state, Forwarding state, Listening state, Learning state, Disabled state, Alternate role, Discarding state, Backup role, Root Port, Designated Port, superior BPDU, inferior BPDU, PVST+, RPVST+, PortFast, Root Guard, BPDU Guard, UDLD, Loop Guard, LACP, PAgP 

Refer to the glossary to check your answers.

## **Further Reading** 

The topics in this chapter tend to be covered in slightly more detail in CCNP Switching exam preparation books. For more details on these topics, refer to the Cisco Press CCNP preparation books found at  www.ciscopress.com/ccnp . 

_Cisco LAN Switching_ , by Kennedy Clark and Kevin Hamilton, covers STP logic and operations in detail. 

More details about UDLD can be found in RFC 5171 and in U.S. Patent No. 7,480,251. 

180  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Cisco.com has an unusually extensive set of high-quality documents covering selected topics from this chapter. Instead of posting the URLs that can change over time, following is  Table  3-14 of selected documents’ names and Document ID numbers you can use in the Search function to locate the appropriate document. So, for example, when looking for “Understanding Spanning Tree Protocol Topology Changes,” type the string “Document ID 12013” in the Search box on the Cisco website. If “PDF” is indicated instead of a numerical Document ID, the document has no Document ID and must be searched for only using its name. Some of the documents cover topics that are outdated and/or have been dropped from the current exam blueprint but which are nevertheless worth reading to reinforce your understanding. Most of the indicated documents are a must-read, though. 

**Table 3-14** _Recommended Further Reading at Cisco.com_ 

|**Table 3-14** _Recommended Further Reading at Cisco.com_||
|---|---|
|**Document Name**|**Document ID**|
|Understanding Spanning-Tree Protocol Topology Changes|12013|
|VLAN Load Balancing Between Trunks Using the Spanning-Tree|10555|
|Protocol Port Priority||
|Understanding and Tuning Spanning Tree Protocol Timers|19120|
|Understanding and Configuring the Cisco UplinkFast Feature|10575|
|Understanding and Configuring Backbone Fast on Catalyst|12014|
|Switches||
|Understanding Rapid Spanning Tree Protocol (802.1w)|24062|
|Understanding Multiple Spanning Tree Protocol (802.1s)|24248|
|PVST Simulation on MST Switches|116464|
|Using PortFast and Other Commands to Fix Workstation Startup|10553|
|Connectivity Delays||
|Spanning Tree PortFast BPDU Guard Enhancement|10586|
|Spanning Tree Protocol Root Guard Enhancement|10588|
|Spanning-Tree Protocol Enhancements using Loop Guard and|10596|
|BPDU Skew Detection Features||
|Understanding and Configuring the Unidirectional Link|10591|
|Detection Protocol Feature||
|Spanning Tree from PVST+ to Rapid-PVST Migration|72836|
|Configuration Example||
|Configuration Example to Migrate Spanning Tree from PVST+ to|72844|
|MST||
|Cisco AVVID Network Infrastructure: Implementing 802.1w and|PDF|
|802.1s in Campus Networks||



Chapter 3: Spanning Tree Protocol  181 

|**Document Name**|**Document ID**|
|---|---|
|Best Practices for Catalyst 6500/6000 Series and Catalyst|24330|
|4500/4000 Series Switches Running Cisco IOS Software||
|Troubleshooting Transparent Bridging Environments|10543|
|Troubleshooting LAN Switching Environments|12006|
|Spanning Tree Protocol Problems and Related Design|10556|
|Considerations||
|Troubleshooting STP on Catalyst Switches Running Cisco IOS|28943|
|System Software||
|Troubleshooting Spanning Tree PVID- and Type-Inconsistencies|24063|
|Understanding EtherChannel Load Balancing and Redundancy on|12023|
|Catalyst Switches||
|Understanding EtherChannel Inconsistency Detection|20625|
|Catalyst 6500, 4500, and 3750 Series Switches EtherChannel|116385|
|Load-Balancing||
|Errdisable Port State Recovery on the Cisco IOS Platforms|69980|




![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0223-00.png)

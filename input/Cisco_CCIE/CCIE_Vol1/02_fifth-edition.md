## **About the Authors** 

**Narbik Kocharians** , CCIE No. 12410 (Routing and Switching, Security, SP), is a Triple CCIE with more than 32 years of experience in the IT industry. He has designed, implemented, and supported numerous enterprise networks. Narbik is the president of Micronics Training Inc. ( www.micronicstraining.com ), where he teaches CCIE R&S and SP boot camps. 

**Peter Palúch** , CCIE No. 23527 (Routing and Switching), is an assistant professor, Cisco Networking Academy instructor, and instructor trainer at the Faculty of Management Science and Informatics, University of Zilina, Slovakia. Peter has cooperated in various educational activities in Slovakia and abroad, focusing on networking and Linux-based network server systems. He is also active at the Cisco Support Community, holding the Cisco Designated VIP award in LAN & WAN Routing and Switching areas since the award program inception in 2011. Upon invitation by Cisco in 2012, Peter joined two Job Task Analysis groups that assisted defining the upcoming CCIE R&S and CCNP R&S certification exam topics. Peter holds an M.Sc. degree in Applied Informatics and a doctoral degree in the area of VoIP quality degradation factors. Together with his students, Peter has started the project of implementing the EIGRP routing protocol into the Quagga open-source routing software suite, and has been driving the effort since its inception in 2013. 

v

## **About the Technical Reviewers** 

**Paul Negron** , CCIE No. 14856, CCSI No. 22752, has been affiliated with networking technologies for 17 years and has been involved with the design of core network services for a number of service providers, such as Comcast, Qwest, British Telecom, and Savvis to name a few. He currently instructs all the CCNP Service Provider–level courses, including Advanced BGP, MPLS, and the QoS course. Paul has six years of experience with satellite communications as well as ten years of experience with Cisco platforms. 

**Sean Wilkins** is an accomplished networking consultant for SR-W Consulting ( www.sr-wconsulting.com ) and has been in the field of IT since the mid 1990s, working with companies such as Cisco, Lucent, Verizon, and AT&T as well as several other private companies. Sean currently holds certifications with Cisco (CCNP/CCDP), Microsoft (MCSE), and CompTIA (A+ and Network+). He also has a Master of Science in information technology with a focus in network architecture and design, a Master of Science in organizational management, a Master’s Certificate in network security, a Bachelor of Science in computer networking, and Associates of Applied Science in computer information systems. In addition to working as a consultant, Sean spends most of his time as a technical writer and editor for various companies; check out this work at his author website:  www.infodispersion.com . 

vi  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Dedications**

## **From Narbik Kocharians:** 

I would like to dedicate this book to my wife, Janet, for her love, encouragement, and continuous support, and to my dad for his words of wisdom.

## **From Peter Palúch:** 

To my family, students, colleagues, and friends. 

vii

## **Acknowledgments**

## **From Narbik Kocharians:** 

First, I would like to thank God for giving me the opportunity and ability to write, teach, and do what I truly enjoy doing. Also, I would like to thank my family, especially my wife of 29 years, Janet, for her constant encouragement and help. She does such an amazing job of interacting with students and handling all the logistics of organizing classes as I focus on teaching. I also would like to thank my children, Chris, Patrick, Alexandra, and my little one, Daniel, for their patience. 

A special thanks goes to Mr. Brett Bartow for his patience and our constant changing of the deadlines. It goes without saying that the technical editors and reviewers did a phenomenal job; thank you very much. Finally, I would like to thank all my students who inspire me every day, and you, for reading this book.

## **From Peter Palúch:** 

The opportunity to cooperate on the new edition of this book has been an honor and privilege beyond words for me. Wendell Odom, who has so gracefully and generously passed the torch to us, was the key person in introducing me to the Cisco Press representatives as a possible author, and I will be forever indebted to him for all the trust he has blessed us with. I have strived very much to live up to the unparalelled high level of content all previous authors have maintained throughout all editions of this book, and I would like to sincerely thank all of them for authoring such a great book that has significantly helped me achieve my certification in the first place. 

My next immense thank you goes to Brett Bartow, the executive editor for this book. Brett’s inviting and forthcoming attitude throughout the time of editing the book, compounded with his patience and understanding for my ever-moving (and constantly missed) deadlines, is second to none. He has done all in his power to help us, the authors, without compromising the quality of the work. 

I would not have been able to complete my work on this volume without the endless support of my family. They have encouraged me, supported me, and gone out of their way to accommodate my needs. Words are not enough to express my gratitude. 

Psalm 127, whose musical setting in works of Monteverdi, Handel, or Vivaldi I have come to admire, begins with words “Unless the Lord build the house, they labor in vain who build.” Indeed, if it was not first and foremost the Lord’s blessing and help throughout, this work would not have been finished successfully. To my Lord and Savior, Jesus Christ—thank you! 

viii  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Contents at a Glance** 

Introduction  xxiv

## **Part I LAN Switching** 

- Chapter 1 Ethernet Basics  3 

- Chapter 2 Virtual LANs and VLAN Trunking  47 

- Chapter 3 Spanning Tree Protocol  103

## **Part II IP Networking** 

- Chapter 4 IP Addressing  183 

- Chapter 5 IP Services  227

## **Part III IP IGP Routing** 

- Chapter 6 IP Forwarding (Routing)  267 

- Chapter 7 RIPv2 and RIPng  313 

- Chapter 8 EIGRP  347 

- Chapter 9 OSPF  453 

- Chapter 10 IS-IS  563 

- Chapter 11 IGP Route Redistribution, Route Summarization, Default Routing, and Troubleshooting  633

## **Part IV Final Preparation** 

- Chapter 12 Final Preparation  701 

**Part V Appendixes** 

- Appendix A   Answers to the “Do I Know This Already?” Quizzes  707 

- Appendix B   CCIE Exam Updates  713 

   - Index 714

## **CD-Only** 

- Appendix C   Decimal to Binary Conversion Table 

- Appendix D   IP Addressing Practice 

- Appendix E   Key Tables for CCIE Study 

- Appendix F   Solutions for Key Tables for CCIE Study 

- Appendix G Study Planner 

   - Glossary 

ix

## **Contents** 

Introduction  xxiv 

**Part I LAN Switching Chapter 1 Ethernet Basics 3** “Do I Know This Already?” Quiz 3 Foundation Topics 8 Ethernet Layer 1: Wiring, Speed, and Duplex 8 RJ-45 Pinouts and Category 5 Wiring 8 Autonegotiation, Speed, and Duplex 9 _CSMA/CD 10 Collision Domains and Switch Buffering 10_ Basic Switch Port Configuration 11 Ethernet Layer 2: Framing and Addressing 14 Types of Ethernet Addresses 16 Ethernet Address Formats 17 Protocol Types and the 802.3 Length Field 18 Switching and Bridging Logic 19 SPAN, RSPAN, and ERSPAN 22 Core Concepts of SPAN, RSPAN, and ERSPAN 23 Restrictions and Conditions 24 Basic SPAN Configuration 26 Complex SPAN Configuration 26 RSPAN Configuration 26 ERSPAN Configuration 27 Virtual Switch System 28 Virtual Switching System 29 VSS Active and VSS Standby Switch 30 Virtual Switch Link 30 Multichassis EtherChannel (MEC) 31 Basic VSS Configuration 31 VSS Verification Procedures 35 IOS-XE 38 Foundation Summary 41 

x  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Memory Builders 44 Fill In Key Tables from Memory 44 Definitions 44 Further Reading 45 **Chapter 2 Virtual LANs and VLAN Trunking 47** “Do I Know This Already?” Quiz 47 Foundation Topics 51 Virtual LANs 51 VLAN Configuration 51 _Using VLAN Database Mode to Create VLANs 52 Using Configuration Mode to Put Interfaces into VLANs 55 Using Configuration Mode to Create VLANs 56 Modifying the Operational State of VLANs 57_ Private VLANs 60 VLAN Trunking: ISL and 802.1Q 69 ISL and 802.1Q Concepts 69 ISL and 802.1Q Configuration 71 _Allowed, Active, and Pruned VLANs 76 Trunk Configuration Compatibility 76_ Configuring Trunking on Routers 77 802.1Q-in-Q Tunneling 79 VLAN Trunking Protocol 83 VTP Process and Revision Numbers 86 VTP Configuration 89 _Normal-Range and Extended-Range VLANs 94_ Storing VLAN Configuration 94 Configuring PPPoE 96 Foundation Summary 99 Memory Builders 101 Fill In Key Tables from Memory 101 Definitions 101 Further Reading 101 

xi 

**Chapter 3 Spanning Tree Protocol 103** 

“Do I Know This Already?” Quiz 103 Foundation Topics 107 802.1D Spanning Tree Protocol and Improvements 107 Choosing Which Ports Forward: Choosing Root Ports and Designated Ports 109 _Electing a Root Switch 110 Determining the Root Port 111 Determining the Designated Port 113_ Converging to a New STP Topology 115 _Topology Change Notification and Updating the CAM 117 Transitioning from Blocking to Forwarding 119_ Per-VLAN Spanning Tree and STP over Trunks 119 STP Configuration and Analysis 124 Rapid Spanning Tree Protocol 128 New Port Roles, States and Types, and New Link Types 128 Changes to BPDU Format and Handling 132 Proposal/Agreement Process in RSTP 133 Topology Change Handling in RSTP 136 Rapid Per-VLAN Spanning Tree Plus (RPVST+) 137 Multiple Spanning Trees: IEEE 802.1s 137 MST Principles of Operation 138 Interoperability Between MST and Other STP Versions 141 MST Configuration 144 Protecting and Optimizing STP 148 PortFast Ports 148 Root Guard, BPDU Guard, and BPDU Filter: Protecting Access Ports 149 Protecting Against Unidirectional Link Issues 151 Configuring and Troubleshooting EtherChannels 154 Load Balancing Across Port-Channels 154 Port-Channel Discovery and Configuration 157 Troubleshooting Complex Layer 2 Issues 161 Layer 2 Troubleshooting Process 162 Layer 2 Protocol Troubleshooting and Commands 163 _Troubleshooting Using Cisco Discovery Protocol 163 Troubleshooting Using Link Layer Discovery Protocol 165 Troubleshooting Using Basic Interface Statistics 167_ 

xii  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Troubleshooting Spanning Tree Protocol 170 _Troubleshooting Trunking 171 Troubleshooting VTP 172 Troubleshooting EtherChannels 174_ Approaches to Resolving Layer 2 Issues 175 Foundation Summary 177 Memory Builders 179 Fill in Key Tables from Memory 179 Definitions 179 Further Reading 179

## **Part II IP Networking**

## **Chapter 4 IP Addressing 183** 

“Do I Know This Already?” Quiz 183 Foundation Topics 187 IP Operation 187 TCP Operation 187 UDP Operation 188 IP Addressing and Subnetting 188 IP Addressing and Subnetting Review 188 _Subnetting a Classful Network Number 189 Comments on Classless Addressing 191_ Subnetting Math 192 _Dissecting the Component Parts of an IP Address 192 Finding Subnet Numbers and Valid Range of IP Addresses— Binary 193 Decimal Shortcuts to Find the Subnet Number and Valid Range of IP Addresses 194 Determining All Subnets of a Network—Binary 196 Determining All Subnets of a Network—Decimal 198_ VLSM Subnet Allocation 200 Route Summarization Concepts 201 _Finding Inclusive Summary Routes—Binary 202 Finding Inclusive Summary Routes—Decimal 203 Finding Exclusive Summary Routes—Binary 204_ 

CIDR, Private Addresses, and NAT 205 Classless Interdomain Routing 206 Private Addressing 207 

xiii 

Network Address Translation 207 _Static NAT 209 Dynamic NAT Without PAT 210 Overloading NAT with Port Address Translation 211 Dynamic NAT and PAT Configuration 212_ IPv6 214 IPv6 Address Format 215 Network Prefix 215 IPv6 Address Types 216 Address Management and Assignment 216 _Static Configuration 217 Stateless Address Autoconfiguration 217 Stateful DHCPv6 217 Stateless DHCP 218_ IPv6 Transition Technologies 218 _Dual Stack 218 Tunneling 219 Translation 220_ Foundation Summary 221 Memory Builders 225 Fill in Key Tables from Memory 225 Definitions 225 Further Reading 225 **Chapter 5 IP Services 227** “Do I Know This Already?” Quiz 227 Foundation Topics 232 ARP, Proxy ARP, Reverse ARP, BOOTP, and DHCP 232 ARP and Proxy ARP 232 RARP, BOOTP, and DHCP 233 DHCP 234 HSRP, VRRP, and GLBP 236 Network Time Protocol 240 SNMP 241 SNMP Protocol Messages 243 SNMP MIBs 244 SNMP Security 245 Syslog 245 

xiv  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Web Cache Communication Protocol 246 Implementing the Cisco IOS IP Service Level Agreement (IP SLA) Feature 249 Implementing NetFlow 250 Implementing Router IP Traffic Export 252 Implementing Cisco IOS Embedded Event Manager 253 Implementing Remote Monitoring 254 Implementing and Using FTP on a Router 255 Implementing a TFTP Server on a Router 256 Implementing Secure Copy Protocol 257 Implementing HTTP and HTTPS Access 257 Implementing Telnet Access 258 Implementing SSH Access 258 Foundation Summary 259 Memory Builders 264 Fill In Key Tables from Memory 264 Definitions 264 Further Reading 264 **Part III IP IGP Routing Chapter 6 IP Forwarding (Routing) 267** “Do I Know This Already?” Quiz 267 Foundation Topics 271 IP Forwarding 271 Process Switching, Fast Switching, and Cisco Express Forwarding 272 Load Sharing with CEF and Related Issues 282 Multilayer Switching 286 MLS Logic 286 Using Routed Ports and Port-channels with MLS 287 MLS Configuration 291 Policy Routing 296 Routing Protocol Changes and Migration 299 Planning the Migration Strategy 300 Activating New IGP While Keeping the Current IGP Intact 300 Verifying New IGP Adjacencies and Working Database Contents 301 Deactivating Current IGP 301 Removing New IGP’s Temporary Settings 303 Specifics of Distance-Vector Protocols in IGP Migration 303 

xv 

Foundation Summary 309 Memory Builders 310 Fill In Key Tables from Memory 310 Definitions 310 Further Reading 310 **Chapter 7 RIPv2 and RIPng 313** “Do I Know This Already?” Quiz 313 Foundation Topics 316 Introduction to Dynamic Routing 316 RIPv2 Basics 318 RIPv2 Convergence and Loop Prevention 320 Converged Steady-State Operation 327 Triggered (Flash) Updates and Poisoned Routes 328 RIPv2 Convergence When Routing Updates Cease 331 Convergence Extras 334 RIPv2 Configuration 334 Enabling RIPv2 and the Effects of Autosummarization 335 RIPv2 Authentication 337 RIPv2 Next-Hop Feature and Split Horizon 338 RIPv2 Offset Lists 338 Route Filtering with Distribute Lists and Prefix Lists 338 RIPng for IPv6 339 Foundation Summary 342 Memory Builders 345 Definitions 345 Further Reading 345 **Chapter 8 EIGRP 347** “Do I Know This Already?” Quiz 347 Foundation Topics 356 EIGRP Basics and Evolution 356 EIGRP Roots: Interior Gateway Routing Protocol 357 Moving from IGRP to Enhanced IGRP 358 EIGRP Metrics, Packets, and Adjacencies 360 EIGRP Classic Metrics 360 _Bandwidth Metric Component 361 Delay Metric Component 361_ 

xvi  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

_Reliability Metric Component 362 Load Metric Component 362 MTU Metric Component 363 Hop Count Metric Component 363 Calculating the Composite Metric 363_ EIGRP Wide Metrics 364 Tweaking Interface Metrics to Influence Path Selection 368 EIGRP Packet Format 368 EIGRP Packets 371 _EIGRP Packets in Action 371 Hello Packets 372 Acknowledgment Packets 372 Update Packets 373 Query Packet 374 Reply Packets 374 SIA-Query and SIA-Reply Packets 374_ Reliable Transport Protocol 374 Router Adjacencies 376 Diffusing Update Algorithm 380 Topology Table 380 Computed, Reported, and Feasible Distances, and Feasibility Condition 384 Local and Diffusing Computations in EIGRP 391 DUAL FSM 397 Stuck-In-Active State 402 EIGRP Named Mode 410 Address Family Section 414 Per-AF-Interface Configuration Section 415 Per-AF-Topology Configuration Section 416 Additional and Advanced EIGRP Features 417 Router ID 417 Unequal-Cost Load Balancing 420 Add-Path Support 421 Stub Routing 423 Route Summarization 427 Passive Interfaces 431 Graceful Shutdown 432 

xvii 

Securing EIGRP with Authentication 432 Default Routing Using EIGRP 435 Split Horizon 436 EIGRP Over the ToP 437 EIGRP Logging and Reporting 443 EIGRP Route Filtering 443 EIGRP Offset Lists 444 Clearing the IP Routing Table 444 Foundation Summary 445 Memory Builders   450 Fill In Key Tables from Memory 450 Definitions 450 Further Reading 450 **Chapter 9 OSPF 453** “Do I Know This Already?” Quiz 453 Foundation Topics 460 OSPF Database Exchange 460 OSPF Router IDs 460 Becoming Neighbors, Exchanging Databases, and Becoming Adjacent 461 _OSPF Neighbor States 462 Becoming Neighbors: The Hello Process 464 Transmitting LSA Headers to Neighbors 466 Database Description Exchange: Master/Slave Relationship 466 Requesting, Getting, and Acknowledging LSAs 468_ Designated Routers on LANs 469 _Designated Router Optimization on LANs 470 DR Election on LANs 471_ Designated Routers on WANs and OSPF Network Types 472 _Caveats Regarding OSPF Network Types over NBMA Networks 474 Example of OSPF Network Types and NBMA 474_ SPF Calculation 479 Steady-State Operation 480 OSPF Design and LSAs 480 OSPF Design Terms 480 OSPF Path Selection Process 482 LSA Types 482 _LSA Types 1 and 2 484 LSA Type 3 and Inter-Area Costs 488_ 

xviii  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

_LSA Types 4 and 5, and External Route Types 1 and 2 492 OSPF Design in Light of LSA Types 496_ Stubby Areas 496 OSPF Path Choices That Do Not Use Cost 502 _Choosing the Best Type of Path 502 Best-Path Side Effects of ABR Loop Prevention 502_ OSPF Configuration 505 OSPF Costs and Clearing the OSPF Process 507 _Alternatives to the OSPF network Command 510_ OSPF Filtering 510 _Filtering Routes Using the distribute-list Command 511 OSPF ABR LSA Type 3 Filtering 513 Filtering Type 3 LSAs with the area range Command 514_ Virtual Link Configuration 515 Configuring Classic OSPF Authentication 517 Configuring Extended Cryptographic OSPF Authentication 520 Protecting OSPF Routers with TTL Security Check 522 Tuning OSPF Performance 523 _Tuning the SPF Scheduling with SPF Throttling 524 Tuning the LSA Origination with LSA Throttling 526 Incremental SPF 527 OSPFv2 Prefix Suppression 528 OSPF Stub Router Configuration 529 OSPF Graceful Restart 530 OSPF Graceful Shutdown 532_ OSPFv3 533 Differences Between OSPFv2 and OSPFv3 533 Virtual Links, Address Summarization, and Other OSPFv3 Features 534 OSPFv3 LSA Types 534 OSPFv3 in NBMA Networks 536 Configuring OSPFv3 over Frame Relay 537 Enabling and Configuring OSPFv3 537 OSPFv3 Authentication and Encryption 546 OSPFv3 Address Family Support 548 OSPFv3 Prefix Suppression 552 OSPFv3 Graceful Shutdown 552 Foundation Summary 553 

xix 

Memory Builders   560 Fill in Key Tables from Memory  560 Definitions  560 Further Reading  561

## **Chapter 10 IS-IS 563** 

“Do I Know This Already?” Quiz 563 Foundation Topics 571 OSI Network Layer and Addressing 572 Levels of Routing in OSI Networks 576 IS-IS Metrics, Levels, and Adjacencies 577 IS-IS Packet Types 579 Hello Packets 579 Link State PDUs 580 Complete and Partial Sequence Numbers PDUs 585 IS-IS Operation over Different Network Types 586 IS-IS Operation over Point-to-Point Links 587 IS-IS Operation over Broadcast Links 592 Areas in IS-IS 598 Authentication in IS-IS 608 IPv6 Support in IS-IS 610 Configuring IS-IS 613 Foundation Summary 625 Memory Builders 629 Fill In Key Tables from Memory 630 Definitions 630 Further Reading 630 **Chapter 11 IGP Route Redistribution, Route Summarization, Default Routing, and Troubleshooting 633** 

“Do I Know This Already?” Quiz 633 Foundation Topics 638 Route Maps, Prefix Lists, and Administrative Distance 638 Configuring Route Maps with the route-map Command 638 _Route Map match Commands for Route Redistribution 640 Route Map set Commands for Route Redistribution 641_ IP Prefix Lists 641 Administrative Distance 644 

xx  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

Route Redistribution 645 Mechanics of the redistribute Command 645 _Redistribution Using Default Settings 646 Setting Metrics, Metric Types, and Tags 649_ Redistributing a Subset of Routes Using a Route Map 650 Mutual Redistribution at Multiple Routers 654 _Preventing Suboptimal Routes by Setting the Administrative Distance 656 Preventing Suboptimal Routes by Using Route Tags 659 Using Metrics and Metric Types to Influence Redistributed Routes 661_ Route Summarization 663 EIGRP Route Summarization 664 OSPF Route Summarization 665 Default Routes 665 Using Static Routes to 0.0.0.0, with redistribute static 667 Using the default-information originate Command 669 Using the ip default-network Command 670 Using Route Summarization to Create Default Routes 671 Performance Routing (PfR) 672 

Performance Routing Operational Phases 673 Performance Routing Concepts 674 Authentication 674 Performance Routing Operational Roles 675 _Master Controller (MC) 675 Border Router 676_ PfR Basic Configuration 677 _Configuration of the Master Controller 677 Configuration of the Border Router 681 Task Completion on R3 682_ Troubleshooting Complex Layer 3 Issues 683 Layer 3 Troubleshooting Process 684 Layer 3 Protocol Troubleshooting and Commands 686 _IP Routing Processes 686_ Approaches to Resolving Layer 3 Issues 695 Foundation Summary 696 

xxi 

Memory Builders 698 Fill In Key Tables from Memory 698 Definitions 698 Further Reading 698 **Part IV Final Preparation Chapter 12 Final Preparation 701** Tools for Final Preparation 701 Pearson Cert Practice Test Engine and Questions on the CD 701 _Install the Software from the CD 701 Activate and Download the Practice Exam 702 Activating Other Exams 702 Premium Edition 703_ The Cisco Learning Network 703 Memory Tables 703 Chapter-Ending Review Tools 704 Suggested Plan for Final Review/Study 704 Using the Exam Engine 704 Summary 705 **Part V Appendixes Appendix A Answers to the “Do I Know This Already?” Quizzes 707 Appendix B CCIE Exam Updates 713 Index 714**

## **CD-Only** 

**Appendix C Decimal to Binary Conversion Table Appendix D IP Addressing Practice Appendix E Key Tables for CCIE Study Appendix F Solutions for Key Tables for CCIE Study Appendix G Study Planner Glossary** 

xxii  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Icons Used in This Book** 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0023-02.png)



![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0023-03.png)



![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0023-04.png)


**----- Start of picture text -----**<br>
Communication PC PC with Sun Macintosh Branch<br>Server Software Workstation Office<br>Headquarters Terminal File  Web Cisco Works House, Regular<br>Server Server Workstation<br>Printer Laptop IBM Label Switch Cluster<br>Mainframe Router Controller<br>Gateway Router Bridge Hub ATM router Cisco<br>MDS 9500<br>Catalyst Multilayer ATM Route/Switch  LAN2LAN<br>Switch Switch Switch Processor Switch<br>Cisco  Optical Enterprise  Fibre  ONS 15540<br>MDS 9500 Services Fibre Channel disk Channel<br>Router JBOD<br>Network Cloud Line: Ethernet Line: Serial Line: Switched Serial<br>**----- End of picture text -----**<br>


xxiii

## **Command Syntax Conventions** 

The conventions used to present command syntax in this book are the same conventions used in the IOS Command Reference. The Command Reference describes these conventions as follows: 

- **Boldface** indicates commands and keywords that are entered literally as shown. In actual configuration examples and output (not general command syntax), boldface indicates commands that are manually input by the user (such as a **show** command). 

- _Italic_ indicates arguments for which you supply actual values. 

- Vertical bars (|) separate alternative, mutually exclusive elements. 

- Square brackets ([ ]) indicate an optional element. 

- Braces ({ }) indicate a required choice. 

- Braces within brackets ([{ }]) indicate a required choice within an optional element. 

xxiv  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1

## **Introduction** 

The Cisco Certified Internetwork Expert (CCIE) certification might be the most challenging and prestigious of all networking certifications. It has received numerous awards and certainly has built a reputation as one of the most difficult certifications to earn in all of the technology world. Having a CCIE certification opens doors professionally and typically results in higher pay and looks great on a resume. 

Cisco currently offers several CCIE certifications. This book covers the version 5.0 exam blueprint topics of the written exam for the CCIE Routing and Switching certification. The following list details the currently available CCIE certifications at the time of this book’s publication; check  www.cisco.com/go/ccie for the latest information. The certifications are listed in the order in which they appear on the web page: 

- CCDE 

- CCIE Collaboration 

- CCIE Data Center 

- CCIE Routing & Switching 

- CCIE Security 

- CCIE Service Provider 

- CCIE Service Provider Operations 

- CCIE Wireless 

Each of the CCDE and CCIE certifications requires the candidate to pass both a written exam and a one-day, hands-on lab exam. The written exam is intended to test your knowledge of theory, protocols, and configuration concepts that follow good design practices. The lab exam proves that you can configure and troubleshoot actual gear.

## **Why Should I Take the CCIE Routing and Switching Written Exam?** 

The first and most obvious reason to take the CCIE Routing and Switching written exam is that it is the first step toward obtaining the CCIE Routing and Switching certification. Also, you cannot schedule a CCIE lab exam until you pass the corresponding written exam. In short, if you want all the professional benefits of a CCIE Routing and Switching certification, you start by passing the written exam. 

The benefits of getting a CCIE certification are varied and include the following: 

- Better pay 

- Career-advancement opportunities 

xxv 

- Applies to certain minimum requirements for Cisco Silver and Gold Channel Partners, as well as those seeking Master Specialization, making you more valuable to Channel Partners 

- Better movement through the problem-resolution process when calling the Cisco TAC 

- Prestige 

- Credibility for consultants and customer engineers, including the use of the Cisco CCIE logo 

The other big reason to take the CCIE Routing and Switching written exam is that it recertifies an individual’s associate-, professional-, and expert-level Cisco certifications, regardless of his or her technology track. Recertification requirements do change, so please verify the requirements at  www.cisco.com/go/certifications .

## **CCIE Routing and Switching Written Exam 400-101** 

The CCIE Routing and Switching written exam, at the time of this writing, consists of a two-hour exam administered at a proctored exam facility affiliated with Pearson VUE ( www.vue.com/cisco ). The exam typically includes approximately 100 multiple-choice questions. No simulation questions are currently part of the written exam. 

As with most exams, everyone wants to know what is on the exam. Cisco provides general guidance as to topics on the exam in the CCIE Routing and Switching written exam blueprint, the most recent copy of which can be accessed from  www.cisco.com/go/ccie . 

Cisco changes both the CCIE written and lab blueprints over time, but Cisco seldom, if ever, changes the exam numbers. However, exactly this change occurred when the CCIE Routing and Switching blueprint was refreshed for v5.0. The previous written exam for v4.0 was numbered 350-001; the v5.0 written exam is identified by 400-101. 

Table  I-1 lists the CCIE Routing and Switching written exam blueprint 5.0 at press time. Table  I-1 also lists the chapters that cover each topic. 

**Table I-1** _CCIE Routing and Switching Written Exam Blueprint_ 

|**Topics**|**Book**|**Book**|
|---|---|---|
||**Volume**|**Chapter**|
|**1.0 Network Principles**|||
|_1.1 Network theory_|||
|1.1.a Describe basic software architecture differences between IOS<br>and IOS XE|||
|1.1.a (i) Control plane and Forwarding plane|1|1|
|1.1.a (ii) Impact on troubleshooting and performance|1|1|
|1.1.a (iii) Excluding a specific platform’s architecture|1|1|



xxvi  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0027-01.png)


**----- Start of picture text -----**<br>
 Topics   Book   Book<br>Volume  Chapter<br> 1.1.b Identify Cisco Express Forwarding concepts<br> 1.1.b (i) RIB, FIB, LFIB, Adjacency table   1   6<br> 1.1.b (ii) Load-balancing hash   1   6<br> 1.1.b (iii) Polarization concept and avoidance   1   6<br> 1.1.c Explain general network challenges<br> 1.1.c (i) Unicast flooding   1   4<br> 1.1.c (ii) Out-of-order packets   1   4<br> 1.1.c (iii) Asymmetric routing   1   4<br> 1.1.c (iv) Impact of micro burst   1   4<br> 1.1.d Explain IP operations<br> 1.1.d (i) ICMP unreachable, redirect   1   4<br> 1.1.d (ii) IPv4 options, IPv6 extension headers   1   4<br> 1.1.d (iii) IPv4 and IPv6 fragmentation   1   4<br> 1.1.d (iv) TTL   1   4<br> 1.1.d (v) IP MTU   1   4<br> 1.1.e Explain TCP operations<br> 1.1.e (i) IPv4 and IPv6 PMTU   1   4<br> 1.1.e (ii) MSS   1   4<br> 1.1.e (iii) Latency   1   4<br> 1.1.e (iv) Windowing   1   4<br> 1.1.e (v) Bandwidth delay product   1   4<br> 1.1.e (vi) Global synchronization   1   4<br> 1.1.e (vii) Options   1   4<br> 1.1.f Explain UDP operations<br> 1.1.f (i) Starvation   1   4<br> 1.1.f (ii) Latency   1   4<br> 1.1.f (iii) RTP/RTCP concepts   1   4<br> 1.2 Network implementation and operation<br> 1.2.a Evaluate proposed changes to a network<br> 1.2.a (i) Changes to routing protocol parameters   1   7–10<br> 1.2.a (ii) Migrate parts of a network to IPv6   1   4<br>**----- End of picture text -----**<br>


xxvii 

|**Topics**|**Book**|**Book**|
|---|---|---|
||**Volume**|**Chapter**|
|1.2.a (iii) Routing protocol migration|1|6|
|1.2.a (iv) Adding multicast support|2|8|
|1.2.a (v) Migrate Spanning Tree Protocol|1|3|
|1.2.a (vi) Evaluate impact of new traffic on existing QoS design|2|3, 4, 5|
|_1.3 Network troubleshooting_|||
|1.3.a Use IOS troubleshooting tools<br>1.3.a (i) debug, conditional debug<br>1.3.a (ii) ping, traceroute with extended options<br>1.3.a (iii) Embedded packet capture<br>1.3.a (iv) Performance monitor<br>1.3.b Apply troubleshooting methodologies<br>1.3.b (i) Diagnose the root cause of networking issues (analyze<br>symptoms, identify and describe root cause)<br>1.3.b (ii) Design and implement valid solutions according to<br>constraints<br>1.3.b (iii) Verify and monitor resolution<br>1.3.c Interpret packet capture<br>1.3.c (i) Using Wireshark trace analyzer<br>1.3.c (ii) Using IOS embedded packet capture<br>**2.0 Layer 2 Technologies**<br>_2.1 LAN switching technologies_<br>2.1.a Implement and troubleshoot switch administration<br>2.1.a (i) Managing the MAC address table<br>2.1.a (ii) errdisable recovery<br>2.1.a (iii) L2 MTU<br>2.1.b Implement and troubleshoot Layer 2 protocols<br>2.1.b (i) CDP, LLDP<br>2.1.b (ii) UDLD<br>2.1.c Implement and troubleshoot VLAN|1<br>1<br>2<br>1<br>1<br>1<br>1<br>2<br>2<br>1<br>1<br>1<br>1<br>1|4<br>4<br>9<br>5<br>11<br>11<br>11<br>9<br>9<br>1<br>3<br>1<br>3<br>3|
|2.1.c (i) Access ports|1|2|
|2.1.c (ii) VLAN database|1|2|
|2.1.c (iii) Normal, extended VLAN, voice VLAN|1|2|



xxviii  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0029-01.png)


**----- Start of picture text -----**<br>
 Topics   Book   Book<br>Volume  Chapter<br> 2.1.d Implement and troubleshoot trunking<br> 2.1.d (i) VTPv1, VTPv2, VTPv3, VTP pruning   1   2<br> 2.1.d (ii) dot1Q   1   2<br> 2.1.d (iii) Native VLAN   1   2<br> 2.1.d (iv) Manual pruning   1   2<br> 2.1.e Implement and troubleshoot EtherChannel<br> 2.1.e (i) LACP, PAgP, manual   1   3<br> 2.1.e (ii) Layer 2, Layer 3   1   3<br> 2.1.e (iii) Load balancing   1   3<br> 2.1.e (iv) EtherChannel misconfiguration guard   1   3<br> 2.1.f Implement and troubleshoot spanning tree<br> 2.1.f (i) PVST+/RPVST+/MST   1   3<br> 2.1.f (ii) Switch priority, port priority, path cost, STP timers   1   3<br> 2.1.f (iii) PortFast, BPDU Guard, BPDU Filter   1   3<br> 2.1.f (iv) Loop Guard, Root Guard   1   3<br> 2.1.g Implement and troubleshoot other LAN switching technologies<br> 2.1.g (i) SPAN, RSPAN, ERSPAN   1   1<br> 2.1.h Describe chassis virtualization and aggregation technologies<br> 2.1.h (i) Multichassis   1   1<br> 2.1.h (ii) VSS concepts   1   1<br> 2.1.h (iii) Alternatives to STP   1   1<br> 2.1.h (iv) Stackwise   1   1<br> 2.1.h (v) Excluding specific platform implementation   1   1<br> 2.1.i Describe spanning-tree concepts<br> 2.1.i (i) Compatibility between MST and RSTP   1   3<br> 2.1.i (ii) STP dispute, STP Bridge Assurance   1   3<br> 2.2 Layer 2 multicast<br> 2.2.a Implement and troubleshoot IGMP<br> 2.2.a (i) IGMPv1, IGMPv2, IGMPv3   2   7<br> 2.2.a (ii) IGMP snooping   2   7<br> 2.2.a (iii) IGMP querier   2   7<br>**----- End of picture text -----**<br>


xxix 

|**Topics**|**Book**|**Book**|
|---|---|---|
||**Volume**|**Chapter**|
|2.2.a (iv) IGMP filter|2|7|
|2.2.a (v) IGMP proxy|2|7|
|2.2.b Explain MLD|2|8|
|2.2.c Explain PIM snooping|2|8|
|_2.3 Layer 2 WAN circuit technologies_|||
|2.3.a Implement and troubleshoot HDLC|2|6|
|2.3.b Implement and troubleshoot PPP<br>2.3.b (i) Authentication (PAP, CHAP)<br>2.3.b (ii) PPPoE<br>2.3.b (iii) MLPPP<br>2.3.c Describe WAN rate-based Ethernet circuits<br>2.3.c (i) Metro and WAN Ethernet topologies<br>2.3.c (ii) Use of rate-limited WAN Ethernet services<br>**3.0 Layer 3 Technologies**<br>_3.1 Addressing technologies_<br>3.1.a Identify, implement, and troubleshoot IPv4 addressing and<br>subnetting<br>3.1.a (i) Address types, VLSM<br>3.1.a (ii) ARP<br>3.1.b Identify, implement, and troubleshoot IPv6 addressing and<br>subnetting<br>3.1.b (i) Unicast, multicast<br>3.1.b (ii) EUI-64<br>3.1.b (iii) ND, RS/RA<br>3.1.b (iv) Autoconfig/SLAAC, temporary addresses (RFC 4941)<br>3.1.b (v) Global prefix configuration feature<br>3.1.b (vi) DHCP protocol operations<br>3.1.b (vii) SLAAC/DHCPv6 interaction<br>3.1.b (viii) Stateful, stateless DHCPv6<br>3.1.b (ix) DHCPv6 prefix delegation<br>_3.2 Layer 3 multicast_<br>3.2.a Troubleshoot reverse path forwarding|2<br>2<br>2<br>2<br>2<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>2<br>1<br>1|6<br>6<br>6<br>6<br>6<br>4<br>4<br>4<br>4<br>4<br>4<br>4<br>4<br>10<br>4<br>4|



xxx  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

|**Topics**|**Book**|**Book**|
|---|---|---|
||**Volume**|**Chapter**|
|3.2.a (i) RPF failure|2|8|
|3.2.a (ii) RPF failure with tunnel interface|2|8|
|3.2.b Implement and troubleshoot IPv4 protocol independent<br>multicast<br>3.2.b (i) PIM dense mode, sparse mode, sparse-dense mode<br>3.2.b (ii) Static RP, auto-RP, BSR<br>3.2.b (iii) Bidirectional PIM<br>3.2.b (iv) Source-specific multicast<br>3.2.b (v) Group-to-RP mapping<br>3.2.b (vi) Multicast boundary<br>3.2.c Implement and troubleshoot multicast source discovery protocol<br>3.2.c (i) Intra-domain MSDP (anycast RP)<br>3.2.c (ii) SA filter<br>3.2.d Describe IPv6 multicast<br>3.2.d (i) IPv6 multicast addresses<br>3.2.d (ii) PIMv6<br>_3.3 Fundamental routing concepts_<br>3.3.a Implement and troubleshoot static routing<br>3.3.b Implement and troubleshoot default routing<br>3.3.c Compare routing protocol types|2<br>2<br>2<br>2<br>2<br>2<br>2<br>2<br>2<br>2<br>1<br>1|8<br>8<br>8<br>8<br>8<br>8<br>8<br>8<br>7<br>8<br>6<br>7–11|
|3.3.c (i) Distance vector|1|7|
|3.3.c (ii) Link state|1|7|
|3.3.c (iii) Path vector|1|7|
|3.3.d Implement, optimize, and troubleshoot administrative distance|1|11|
|3.3.e Implement and troubleshoot passive interface|1|7–10|
|3.3.f Implement and troubleshoot VRF lite|2|11|
|3.3.g Implement, optimize, and troubleshoot filtering with any routing|1|11|
|protocol|||
|3.3.h Implement, optimize, and troubleshoot redistribution between|1|11|
|any routing protocols|||
|3.3.i Implement, optimize, and troubleshoot manual and auto|1|7–10|
|summarization with any routing protocol|||



xxxi 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0032-01.png)


**----- Start of picture text -----**<br>
 Topics   Book   Book<br>Volume  Chapter<br> 3.3.j Implement, optimize, and troubleshoot policy-based routing   1   6<br> 3.3.k Identify and troubleshoot suboptimal routing   1   11<br> 3.3.l Implement and troubleshoot bidirectional forwarding detection   1   11<br> 3.3.m Implement and troubleshoot loop prevention mechanisms<br> 3.3.m (i) Route tagging, filtering   1   11<br> 3.3.m (ii) Split horizon   1   7<br> 3.3.m (iii) Route poisoning   1   7<br> 3.3.n Implement and troubleshoot routing protocol authentication<br> 3.3.n (i) MD5   1   7–10<br> 3.3.n (ii) Key-chain   1   7–10<br> 3.3.n (iii) EIGRP HMAC SHA2-256bit   1   8<br> 3.3.n (iv) OSPFv2 SHA1-196bit   1   9<br> 3.3.n (v) OSPFv3 IPsec authentication   1   9<br> 3.4 RIP (v2 and v6)<br> 3.4.a Implement and troubleshoot RIPv2   1   7<br> 3.4.b Describe RIPv6 (RIPng)   1   7<br> 3.5 EIGRP (for IPv4 and IPv6)<br> 3.5.a Describe packet types<br> 3.5.a (i) Packet types (hello, query, update, and so on)   1   8<br> 3.5.a (ii) Route types (internal, external)   1   8<br> 3.5.b Implement and troubleshoot neighbor relationship<br> 3.5.b (i) Multicast, unicast EIGRP peering   1   8<br> 3.5.b (ii) OTP point-to-point peering   1   8<br> 3.5.b (iii) OTP route-reflector peering   1   8<br> 3.5.b (iv) OTP multiple service providers scenario   1   8<br> 3.5.c Implement and troubleshoot loop-free path selection<br> 3.5.c (i) RD, FD, FC, successor, feasible successor   1   8<br> 3.5.c (ii) Classic metric   1   8<br> 3.5.c (iii) Wide metric   1   8<br> 3.5.d Implement and troubleshoot operations<br> 3.5.d (i) General operations   1   8<br>**----- End of picture text -----**<br>


xxxii  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0033-01.png)


**----- Start of picture text -----**<br>
 Topics   Book   Book<br>Volume  Chapter<br> 3.5.d (ii) Topology table, update, query, active, passive   1   8<br> 3.5.d (iii) Stuck in active   1   8<br> 3.5.d (iv) Graceful shutdown   1   8<br> 3.5.e Implement and troubleshoot EIGRP stub<br> 3.5.e (i) Stub   1   8<br> 3.5.e (ii) Leak-map   1   8<br> 3.5.f Implement and troubleshoot load balancing<br> 3.5.f (i) equal-cost   1   8<br> 3.5.f (ii) unequal-cost   1   8<br> 3.5.f (iii) add-path   1   8<br> 3.5.g Implement EIGRP (multiaddress) named mode<br> 3.5.g (i) Types of families   1   8<br> 3.5.g (ii) IPv4 address-family   1   8<br> 3.5.g (iii) IPv6 address-family   1   8<br> 3.5.h Implement, troubleshoot, and optimize EIGRP convergence and<br>scalability<br> 3.5.h (i) Describe fast convergence requirements   1   8<br> 3.5.h (ii) Control query boundaries   1   8<br> 3.5.h (iii) IP FRR/fast reroute (single hop)  1 8<br> 3.5.h (iv) Summary leak-map   1   8<br> 3.5.h (v) Summary metric   1   8<br> 3.6 OSPF (v2 and v3)<br> 3.6.a Describe packet types<br> 3.6.a (i) LSA types (1, 2, 3, 4, 5, 7, 9)   1   9<br> 3.6.a (ii) Route types (N1, N2, E1, E2)   1   9<br> 3.6.b Implement and troubleshoot neighbor relationship   1   9<br> 3.6.c Implement and troubleshoot OSPFv3 address-family support<br> 3.6.c (i) IPv4 address-family   1   9<br> 3.6.c (ii) IPv6 address-family   1   9<br> 3.6.d Implement and troubleshoot network types, area types, and<br>router types<br> 3.6.d (i) Point-to-point, multipoint, broadcast, nonbroadcast   1   9<br>**----- End of picture text -----**<br>


xxxiii 

|**Topics**|**Book**|**Book**|
|---|---|---|
||**Volume**|**Chapter**|
|3.6.d (ii) LSA types, area type: backbone, normal, transit, stub, NSSA,|1|9|
|totally stub|||
|3.6.d (iii) Internal router, ABR, ASBR|1|9|
|3.6.d (iv) Virtual link|1|9|
|3.6.e Implement and troubleshoot path preference|1|9|
|3.6.f Implement and troubleshoot operations<br>3.6.f (i) General operations<br>3.6.f (ii) Graceful shutdown<br>3.6.f (iii) GTSM (Generic TTL Security Mechanism)<br>3.6.g Implement, troubleshoot, and optimize OSPF convergence and<br>scalability<br>3.6.g (i) Metrics<br>3.6.g (ii) LSA throttling, SPF tuning, fast hello<br>3.6.g (iii) LSA propagation control (area types, ISPF)<br>3.6.g (iv) IP FRR/fast reroute (single hop)<br>3.6.g (v) LFA/loop-free alternative (multihop)<br>3.6.g (vi) OSPFv3 prefix suppression<br>_3.7 BGP_<br>3.7.a Describe, implement, and troubleshoot peer relationships<br>3.7.a (i) Peer-group, template<br>3.7.a (ii) Active, passive<br>3.7.a (iii) States, timers<br>3.7.a (iv) Dynamic neighbors<br>3.7.b Implement and troubleshoot IBGP and EBGP<br>3.7.b (i) EBGP, IBGP<br>3.7.b (ii) 4-byte AS number<br>3.7.b (iii) Private AS<br>3.7.c Explain attributes and best-path selection<br>3.7.d Implement, optimize, and troubleshoot routing policies|1<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>2<br>2<br>2<br>2<br>2<br>2<br>2<br>2|9<br>9<br>9<br>9<br>9<br>9<br>9<br>9<br>9<br>1<br>1<br>1<br>1<br>1<br>1<br>1<br>1|
|3.7.d (i) Attribute manipulation|2|2|
|3.7.d (ii) Conditional advertisement|2|2|
|3.7.d (iii) Outbound route filtering|2|2|



xxxiv  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0035-01.png)


**----- Start of picture text -----**<br>
 Topics   Book   Book<br>Volume  Chapter<br> 3.7.d (iv) Communities, extended communities   2   2<br> 3.7.d (v) Multihoming   2   2<br> 3.7.e Implement and troubleshoot scalability<br> 3.7.e (i) Route-reflector, cluster   2   2<br> 3.7.e (ii) Confederations   2   2<br> 3.7.e (iii) Aggregation, AS set   2   2<br> 3.7.f Implement and troubleshoot multiprotocol BGP<br> 3.7.f (i) IPv4, IPv6, VPN address-family   2   2<br> 3.7.g Implement and troubleshoot AS path manipulations<br> 3.7.g (i) Local AS, allow AS in, remove private AS   2   2<br> 3.7.g (ii) Prepend   2   2<br> 3.7.g (iii) Regexp   2   2<br> 3.7.h Implement and troubleshoot other features<br> 3.7.h (i) Multipath   2   2<br> 3.7.h (ii) BGP synchronization   2   2<br> 3.7.h (iii) Soft reconfiguration, route refresh   2   2<br> 3.7.i Describe BGP fast convergence features<br> 3.7.i (i) Prefix independent convergence   2   2<br> 3.7.i (ii) Add-path   2   2<br> 3.7.i (iii) Next-hop address tracking   2   2<br> 3.8 IS-IS (for IPv4 and IPv6)<br> 3.8.a Describe basic IS-IS network<br> 3.8.a (i) Single area, single topology   1   10<br> 3.8.b Describe neighbor relationship   1   10<br> 3.8.c Describe network types, levels, and router types<br> 3.8.c (i) NSAP addressing   1   10<br> 3.8.c (ii) Point-to-point, broadcast   1   10<br> 3.8.d Describe operations   1   10<br> 3.8.e Describe optimization features<br> 3.8.e (i) Metrics, wide metric   1   10<br> 4.0 VPN Technologies<br>**----- End of picture text -----**<br>


xxxv 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0036-01.png)


**----- Start of picture text -----**<br>
 Topics   Book   Book<br>Volume  Chapter<br> 4.1 Tunneling<br> 4.1.a Implement and troubleshoot MPLS operations<br> 4.1.a (i) Label stack, LSR, LSP   2   11<br> 4.1.a (ii) LDP   2   11<br> 4.1.a (iii) MPLS ping, MPLS traceroute   2   11<br> 4.1.b Implement and troubleshoot basic MPLS L3VPN<br> 4.1.b (i) L3VPN, CE, PE, P   2   11<br> 4.1.b (ii) Extranet (route leaking)   2   11<br> 4.1.c Implement and troubleshoot encapsulation<br> 4.1.c (i) GRE  2 10<br> 4.1.c (ii) Dynamic GRE  2 10<br> 4.1.c (iii) LISP encapsulation principles supporting EIGRP OTP   1   8<br> 4.1.d Implement and troubleshoot DMVPN (single hub)<br> 4.1.d (i) NHRP   2   10<br> 4.1.d (ii) DMVPN with IPsec using preshared key   2   10<br> 4.1.d (iii) QoS profile   2   10<br> 4.1.d (iv) Pre-classify   2   10<br> 4.1.e Describe IPv6 tunneling techniques<br> 4.1.e (i) 6in4, 6to4   2   8<br> 4.1.e (ii) ISATAP   2   8<br> 4.1.e (iii) 6RD   2   8<br> 4.1.e (iv) 6PE/6VPE   2   8<br> 4.1.g Describe basic Layer 2 VPN—wireline<br> 4.1.g (i) L2TPv3 general principles   2  10<br> 4.1.g (ii) ATOM general principles   2  11<br> 4.1.h Describe basic L2VPN—LAN services<br> 4.1.h (i) MPLS-VPLS general principles   2   10<br> 4.1.h (ii) OTV general principles   2   10<br> 4.2 Encryption<br> 4.2.a Implement and troubleshoot IPsec with preshared key<br> 4.2.a (i) IPv4 site to IPv4 site   2   10<br>**----- End of picture text -----**<br>


xxxvi  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

|**Topics**|**Book**|**Book**|
|---|---|---|
||**Volume**|**Chapter**|
|4.2.a (ii) IPv6 in IPv4 tunnels|2|10|
|4.2.a (iii) Virtual tunneling Interface (VTI)|2|10|
|4.2.b Describe GET VPN|2|10|
|**5.0 Infrastructure Security**|||
|_5.1 Device security_|||
|5.1.a Implement and troubleshoot IOS AAA using local database|2|9|
|5.1.b Implement and troubleshoot device access control<br>5.1.b (i) Lines (VTY, AUX, console)<br>5.1.b (ii) SNMP<br>5.1.b (iii) Management plane protection<br>5.1.b (iv) Password encryption<br>5.1.c Implement and troubleshoot control plane policing<br>5.1.d Describe device security using IOS AAA with TACACS+ and<br>RADIUS<br>5.1.d (i) AAA with TACACS+ and RADIUS<br>5.1.d (ii) Local privilege authorization fallback<br>_5.2 Network security_<br>5.2.a Implement and troubleshoot switch security features<br>5.2.a (i) VACL, PACL<br>5.2.a (ii) Stormcontrol<br>5.2.a (iii) DHCP snooping<br>5.2.a (iv) IP source-guard<br>5.2.a (v) Dynamic ARP inspection<br>5.2.a (vi) port-security<br>5.2.a (vii) Private VLAN<br>5.2.b Implement and troubleshoot router security features<br>5.2.b (i) IPv4 access control lists (standard, extended, time-based)<br>5.2.b (ii) IPv6 traffic filter<br>5.2.b (iii) Unicast reverse path forwarding<br>5.2.c Implement and troubleshoot IPv6 first-hop security|1<br>1<br>2<br>1<br>2<br>2<br>2<br>2<br>2<br>2<br>2<br>2<br>2<br>1<br>2<br>2<br>2|5<br>5<br>9<br>5<br>9<br>9<br>9<br>9<br>9<br>9<br>9<br>9<br>9<br>2<br>9<br>9<br>9|
|5.2.c (i) RA guard|2|9|



xxxvii 

|**Topics**|**Book**|**Book**|
|---|---|---|
||**Volume**|**Chapter**|
|5.2.c (ii) DHCP guard|2|9|
|5.2.c (iii) Binding table|2|9|
|5.2.c (iv) Device tracking|2|9|
|5.2.c (v) ND inspection/snooping|2|9|
|5.2.c (vii) Source guard|2|9|
|5.2.c (viii) PACL|2|9|
|5.2.d Describe 802.1x<br>5.2.d (i) 802.1x, EAP, RADIUS<br>5.2.d (ii) MAC authentication bypass<br>**6.0 Infrastructure Services**<br>_6.1 System management_<br>6.1.a Implement and troubleshoot device management<br>6.1.a (i) Console and VTY<br>6.1.a (ii) Telnet, HTTP, HTTPS, SSH, SCP<br>6.1.a (iii) (T)FTP<br>6.1.b Implement and troubleshoot SNMP<br>6.1.b (i) v2c, v3<br>6.1.c Implement and troubleshoot logging<br>6.1.c (i) Local logging, syslog, debug, conditional debug<br>6.1.c (ii) Timestamp<br>_6.2 Quality of service_<br>6.2.a Implement and troubleshoot end-to-end QoS<br>6.2.a (i) CoS and DSCP mapping<br>6.2.b Implement, optimize, and troubleshoot QoS using MQC|2<br>2<br>1<br>1<br>1<br>1<br>1<br>2<br>2|9<br>9<br>5<br>5<br>5<br>5<br>5<br>6<br>3|
|6.2.b (i) Classification|2|3|
|6.2.b (ii) Network-based application recognition (NBAR)|2|3|
|6.2.b (iii) Marking using IP precedence, DSCP, CoS, ECN|2|3|
|6.2.b (iv) Policing, shaping|2|5|
|6.2.b (v) Congestion management (queuing)|2|4|
|6.2.b (vi) HQoS, subrate Ethernet link|2|3, 4, 5|
|6.2.b (vii) Congestion avoidance (WRED)|2|4|



xxxviii  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0039-01.png)


**----- Start of picture text -----**<br>
 Topics   Book   Book<br>Volume  Chapter<br> 6.2.c Describe Layer 2 QoS<br> 6.2.c (i) Queuing, scheduling   2   4<br> 6.2.c (ii) Classification, marking   2   2<br> 6.3 Network services<br> 6.3.a Implement and troubleshoot first-hop redundancy protocols<br> 6.3.a (i) HSRP, GLBP, VRRP   1   5<br> 6.3.a (ii) Redundancy using IPv6 RS/RA   1   5<br> 6.3.b Implement and troubleshoot Network Time Protocol<br> 6.3.b (i) NTP master, client, version 3, version 4   1   5<br> 6.3.b (ii) NTP Authentication   1   5<br> 6.3.c Implement and troubleshoot IPv4 and IPv6 DHCP<br> 6.3.c (i) DHCP client, IOS DHCP server, DHCP relay   1   5<br> 6.3.c (ii) DHCP options   1   5<br> 6.3.c (iii) DHCP protocol operations   1   5<br> 6.3.c (iv) SLAAC/DHCPv6 interaction   1   4<br> 6.3.c (v) Stateful, stateless DHCPv6   1   4<br> 6.3.c (vi) DHCPv6 prefix delegation   1   4<br> 6.3.d Implement and troubleshoot IPv4 Network Address Translation<br> 6.3.d (i) Static NAT, dynamic NAT, policy-based NAT, PAT   1   5<br> 6.3.d (ii) NAT ALG   2  10<br> 6.3.e Describe IPv6 Network Address Translation<br> 6.3.e (i) NAT64   2  10<br> 6.3.e (ii) NPTv6   2  10<br> 6.4 Network optimization<br> 6.4.a Implement and troubleshoot IP SLA<br> 6.4.a (i) ICMP, UDP, jitter, VoIP   1   5<br> 6.4.b Implement and troubleshoot tracking object<br> 6.4.b (i) Tracking object, tracking list   1   5<br> 6.4.b (ii) Tracking different entities (for example, interfaces, routes,   1   5<br>IPSLA, and so on)<br> 6.4.c Implement and troubleshoot NetFlow<br>**----- End of picture text -----**<br>


xxxix 

|**Topics**|**Book**|**Book**|
|---|---|---|
||**Volume**|**Chapter**|
|6.4.c (i) NetFlow v5, v9|1|5|
|6.4.c (ii) Local retrieval|1|5|
|6.4.c (iii) Export (configuration only)|1|5|
|6.4.d Implement and troubleshoot embedded event manager<br>6.4.d (i) EEM policy using applet<br>6.4.e Identify performance routing (PfR)|1|5|
|6.4.e (i) Basic load balancing|1|11|
|6.4.e (ii) Voice optimization|1|11|



To give you practice on these topics, and pull the topics together, Edition 5 of the _CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1_ includes a large set of CD questions that mirror the types of questions expected for the Version 5.0 blueprint. By their very nature, these topics require the application of the knowledge listed throughout the book. This special section of questions provides a means to learn and practice these skills with a proportionally larger set of questions added specifically for this purpose. 

These questions will be available to you in the practice test engine database, whether you take full exams or choose questions by category.

## **About the** _**CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1**_ **, Fifth Edition** 

This section provides a brief insight into the contents of the book, the major goals, and some of the book features that you will encounter when using this book.

## **Book Organization** 

This volume contains four major parts. Beyond the chapters in these parts of the book, you will find several useful appendixes gathered in  Part  V . 

Following is a description of each part’s coverage: 

- Part  I , “LAN Switching” ( Chapters  1 – 3 ) 

This part focuses on LAN Layer 2 features, specifically Ethernet ( Chapter  1 ), VLANs and trunking ( Chapter  2 ), and Spanning Tree Protocol ( Chapter  3 ). 

- Part  II , “IP Networking” ( Chapters  4 – 5 ) 

This part covers details across the spectrum of the TCP/IP protocol stack. It includes Layer 3 basics ( Chapter  4 ) and IP services such as DHCP and ARP ( Chapter  5 ). 

xl  CCIE Routing and Switching v5.0 Official Cert Guide, Volume 1 

- Part  III , “IP IGP Routing” ( Chapters  6 – 11 ) 

This part covers some of the more important topics on the exam and is easily the largest part of this volume. It covers Layer 3 forwarding concepts ( Chapter  6 ), followed by three routing protocol chapters, one each about RIPv2, EIGRP, OSPF, and IS-IS ( Chapters  7 through  10 , respectively), and concludes with a discussion of IGP redistribution and routing information optimization ( Chapter  11 ). 

- Part  IV , “Final Preparation” 

Chapter  12 , “Final Preparation,” contains instructions about using the testing software on the CD to verify your knowledge, presents suggestions on approaching your studies, and includes hints about further expanding your knowledge by participating in the Cisco Learning Network. 

- Part  V , “Appendixes” 

   - Appendix  A , “Answers to the ‘Do I Know This Already?’ Quizzes”—This appendix lists answers and explanations for the questions at the beginning of each chapter. 

   - Appendix  B , “Exam Updates”—As of the first printing of the book, this appendix contains only a few words that reference the web page for this book, at www.ciscopress.com/title/9781587143960 . As the blueprint evolves over time, the authors will post new materials at the website. Any future printings of the book will include the latest newly added materials in printed form in  Appendix B . If Cisco releases a major exam update, changes to the book will be available only in a new edition of the book and not on this site. 

**Note** Appendixes C, D, E, F, and G and the Glossary are in printable, PDF format on the CD. 

- Appendix  C , “Decimal to Binary Conversion Table” (CD-only)—This appendix lists the decimal values 0 through 255, with their binary equivalents. 

- Appendix  D , “IP Addressing Practice” (CD-only)—This appendix lists several practice problems for IP subnetting and finding summary routes. The explanations to the answers use the shortcuts described in the book. 

- Appendix  E , “Key Tables for CCIE Study” (CD-only)—This appendix lists the most important tables from the core chapters of the book. The tables have much of the content removed so that you can use them as an exercise. You can print the PDF file and then fill in the table from memory, checking your answers against the completed tables in  Appendix  F . 

- Appendix G, “Study Planner” (CD-only)—This appendix is a spreadsheet with major study milestones, where you can track your progress through your study. 

- Glossary (CD-only)—The Glossary contains the key terms listed in the book. 

xli

## **Book Features** 

The core chapters of this book have several features that help you make the best use of your time: 

- **“Do I Know This Already?” Quizzes:** Each chapter begins with a quiz that helps you to determine the amount of time you need to spend studying that chapter. If you score yourself strictly, and you miss only one question, you might want to skip the core of the chapter and move on to the “Foundation Summary” section at the end of the chapter, which lets you review facts and spend time on other topics. If you miss more than one, you might want to spend some time reading the chapter or at least reading sections that cover topics about which you know you are weaker. 

- **Foundation Topics:** These are the core sections of each chapter. They explain the protocols, concepts, and configuration for the topics in that chapter. 

- **Foundation Summary:** The “Foundation Summary” section of this book departs from the typical features of the “Foundation Summary” section of other Cisco Press Exam Certification Guides. This section does not repeat any details from the “Foundation Topics” section; instead, it simply summarizes and lists facts related to the chapter but for which a longer or more detailed explanation is not warranted. 

- **Key topics:** Throughout the “Foundation Topics” section, a Key Topic icon has been placed beside the most important areas for review. After reading a chapter, when doing your final preparation for the exam, take the time to flip through the chapters, looking for the Key Topic icons, and review those paragraphs, tables, figures, and lists. 

- **Fill In Key Tables from Memory:** The more important tables from the chapters have been copied to PDF files available on the CD as  Appendix  E . The tables have most of the information removed. After printing these mostly empty tables, you can use them to improve your memory of the facts in the table by trying to fill them out. This tool should be useful for memorizing key facts. That same CD-only appendix contains the completed tables so that you can check your work. 

- **CD-based practice exam:** The companion CD contains multiple-choice questions and a testing engine. The CD includes 200 questions unique to the CD. As part of your final preparation, you should practice with these questions to help you get used to the exam-taking process, as well as to help refine and prove your knowledge of the exam topics. 

- **Key terms and Glossary:** The more important terms mentioned in each chapter are listed at the end of each chapter under the heading “Definitions.” The Glossary, found on the CD that comes with this book, lists all the terms from the chapters. When studying each chapter, you should review the key terms, and for those terms about which you are unsure of the definition, you can review the short definitions from the Glossary. 

- **Further Reading:** Most chapters include a suggested set of books and websites for additional study on the same topics covered in that chapter. Often, these references will be useful tools for preparation for the CCIE Routing and Switching lab exam. 


![](/tmp/tmpa9v9hzz5/CCIE_Routing_and_Switching_v5.0_Official_Cert_Guide,_Volume_1_-5th_Edition-.pdf-0043-00.png)

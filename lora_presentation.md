# LoRa & MeshCore


<style>
img[alt~="ctr"] {
  display: block;
  margin: 0 auto;
}

table { 
    margin: 0 auto
}

</style>



## Mesh Networking in the Lower South Island

*Jonah Duckles / ZL4EKA*
Presented at ZL4AA - Dunedin Amateur Radio Club Branch 30 NZART
*April 30, 2026*
[jonah@duckles.org](mailto:jonah@duckles.org)

---

![width:600 ctr](https://pad.duckles.nz/uploads/34e3ee8e-88b3-4fcd-bd86-a3e04716a767.png)


---

## Agenda

- What is LoRa?
- Terminology & Technical Basics
- Spectrum & Regulations
- Chirp Spread Spectrum Explained
- Hardware Options
- Local Mesh Status
- Live Demo: Meshtastic App
- Getting Started

---

# What is LoRa?

----

## LoRa 

**Lo**ng **Ra**nge wireless communication protocol

- Low power consumption
- Long range (2-10km urban, 15-40km+ rural)
- Lowish bandwidth 
- License-free ISM bands (We're using 915MHz ISM)
- Perfect for IoT and mesh messaging

----

## LoRa vs LoRaWAN

| LoRa | LoRaWAN |
|------|---------|
| Physical layer | Network protocol |
| Point-to-point | Star topology |
| Peer-to-peer capable | Gateway-based |
| **Community Meshes use LoRa** | Commercial IoT |

----

## Why LoRa for Mesh?

- ✅ Works without infrastructure
- ✅ Modest battery can last days/weeks
- ✅ Free to use (ISM bands)
- ✅ Affordable hardware
- ❌ Not for high-bandwidth applications

The way we are using it this is NOT a ham radio mode. Though there are VERY interesting things going on with APRS LoRa on 70cm. Stay tuned! 

----

## LoRA's place in the modern world of RF

![width:1000px ctr](https://pad.duckles.nz/uploads/d1005f7e-7a95-4fb4-a6d0-b1c0457ad647.png)

---

# Frequency Bands & Regulations

----

## ISM Bands Available

| Region | Frequency | Power Limit | Duty Cycle |
|--------|-----------|-------------|------------|
| NZ/AU | 915-928 MHz | 30 dBm EIRP | 100% |
| EU | 868 MHz | 14 dBm | 1-10% |
| US | 902-928 MHz | 30 dBm | 100% |
| Asia | 433 MHz | Varies | Varies |

**New Zealand**: We use the 915 MHz band (ANZ region)

Note: We're fortunate in NZ to have no duty cycle restrictions on 915 MHz, unlike Europe. This means better mesh performance.

----

## Power Limits & Antenna Gain

**NZ Regulations (915 MHz ISM)**:
- 30 dBm EIRP maximum
- EIRP = Transmit Power + Antenna Gain - Cable Loss

EIRP - Effective Isotropic Radiated Power 

**Example**:
- 22 dBm transmit (158 mW)
- 8 dBi antenna
- 30 dBm EIRP ✅


---

# Chirp Spread Spectrum

----

## What is CSS?

We're trading off sensitivity and data rate while operating in a fixed-bandwidth channel (62.5-500kHz)

**Chirp Spread Spectrum** = LoRa's secret sauce

- Frequency "chirps" sweep across bandwidth
- Encodes data in chirp timing/frequency
- Extremely noise-resistant 
- Can decode signals below noise floor
- Trade-off: bitrate / speed vs. range vs. reliability

---


![width:800 ctr](https://pad.duckles.nz/uploads/4285e350-a8fa-4d7e-a9bc-b8f83533e215.png)


----

![width:900 ctr](https://pad.duckles.nz/uploads/394c86f4-c2fb-4a13-be90-457431b1fc4b.gif)

----

![width:900 ctr](https://pad.duckles.nz/uploads/3f35ca33-8c44-4b5d-8496-40402b328e33.png)

----

![width:900 ctr](https://pad.duckles.nz/uploads/dc511b0a-4c85-4017-99c4-040736d46af0.gif)

----

**Recap:**
- Spreading factor causes more time-on-air, thus more power use and more processing
- However, SF 11 signal resolving power is 😱
- The magic of signal processing 
  - Multiply down-chirp to get constant tone, 
  - FFT to pull out tones as symbols
- Spreading Factors do not interfere with each other

---

Actual repeater update packet 

![width:1000 ctr](https://pad.duckles.nz/uploads/7761b32c-59cd-48a0-906b-0d3d5b73e781.png)

Captured using SDR++ on a HackRF (note LoRa preamble followed by data chips)

---


![width:280 ctr](https://pad.duckles.nz/uploads/9704a237-99cf-4cd3-8101-8fb261563718.png)


---

# Open Mesh Network Firmwares

----

## Open Mesh network firmwares

These are community developed open source projects that are using the low-cost, low-power hardware has created a flourishing in software / firmware experimentation with this hardware. 

- [MeshCore](https://meshcore.io) - Newest kid on the block based on failure modes of meshtastic
- [Meshtastic](http://meshtastic.org) - been around a bit longer, but has some fundamental design flaws. 
- [Reticulum](https://reticulum.network/) - a tool for building networks, including LoRa

----

## Some MeshCore terms 

- **Companion Node**: Individual device on the mesh which is usually bluetooth paired to an app on your phone.
- **Repeater**: A fixed node that extends local / regional coverage.
- **Room Server**: A caching node that saves the last 32 messages for forwarding to nodes that have been offline.
- **Hop**: Message relay between nodes

----

## MeshCore Presets in New Zealand

| Preset           | Spreading Factor | Channel | Coding Rate |
| ---------------- | ---------------- | ------- | ----------- |
| NZ Narrow Preset | 7                | 62.5kHz | 5           |
| NZ Preset        | 11               | 250kHz  | 5           |

---

# Hardware Options

----

## LoRa Devices 

- Have a microcontroller - 
    - ESP32 variant - higher power consumption (though creative power management firmwares are closing this gap)
    - nRF vairant - MUCH lower power consumption 
- Have an RF board, these days often the [SEMTECH SX1262](https://semtech.my.salesforce.com/sfc/p/#E0000000JelG/a/RQ000008nKCH/hp2iKwMDKWl34g1D3LBf_zC7TGBRIo2ff5LMnS8r19s)
- Using the SPI (Serial Peripheral Interface) I/O you can drive a SEMTECH board with anything you want.

----

![width:900 ctr](https://pad.duckles.nz/uploads/e8b0a570-7570-425c-8eed-a8747211b342.png)

----

## SX1262 is enabling this low-cost, low-power boom in hardware

SX1262

- Current recommended chip
- 150-960 MHz
- Much lower power (~5mA RX vs ~100mA)
- Better sensitivity (-148 dBm vs -137 dBm)
- Longer range potential
- ✅ This is what you want in new hardware at the moment

----

## Hardware

| ESP32-based | nRF52-based |
|-------------|-------------|
| • More common<br>• WiFi + Bluetooth<br>• Cheaper<br>• More board options<br>• Higher power consumption | • Lower power (better battery)<br>• Bluetooth only (no WiFi)<br>• Fewer options<br>• Better for solar/portable |



----

## Popular ESP32 Boards

| Feature | TTGO T-Beam | Heltec V3 |
|---------|-------------|-----------|
| **GPS** | ✅ Included | ❌ Not included |
| **Battery** | 18650 battery | Not specified |
| **Display** | OLED display option | ✅ Built-in display |
| **Form Factor** | Complete package | Compact |
| **Antenna** | Standard connector | Good antenna connector |
| **Price Range** | ~$25-35 USD | ~$20-30 USD |
| **Best Use Case** | Most popular - complete solution | Great for portable nodes |

----

## Popular nRF52 Boards

**RAK4631 WisBlock**
- Best nRF option
- Modular (can include screen, sensors and/or GPS for more cost)
- Excellent battery life
- ~$40+ USD




----

## GPS: Yes or No?

**Pros**:
- Position sharing
- Mapping capabilities
- Time synchronization
- Useful for mobile nodes

**Cons**:
- Higher power draw
- Not needed for fixed repeaters
- Privacy considerations

**Recommendation**: Yes for portable, optional for fixed (but can be good for clock sync)

----

## Display Options

<div style="font-size:14px">

| Feature | OLED (0.96" / 1.3") | E-Ink | None |
|---------|---------------------|-------|------|
| **Message Display** | ✅ Shows messages | ✅ Shows messages | ❌ Phone/computer only |
| **Node Stats** | ✅ Shows node stats | ✅ Shows node stats | ❌ Phone/computer only |
| **Battery Level** | ✅ Shows battery level | ✅ Shows battery level | ❌ Phone/computer only |
| **Power Consumption** | Standard | Lower power | Lowest power |
| **Sunlight Readability** | Standard | ✅ Readable in sunlight | N/A |
| **Refresh Rate** | Fast | Slower refresh | N/A |
| **Cost** | Adds ~$5-10 | More expensive | Cheapest |
| **Best Use Case** | General purpose display | Outdoor/solar applications | Budget builds |


</div>

----

## Antenna Considerations

**Stock antennas**: Usually adequate for testing or around the house / town usage

RAK kits come with a panel antenna for both 900MHz and Blutooth. 

**Upgrades**:
- 3-5 dBi: Good all-around
- 6+ dBi: Fixed repeaters 

**Connector types**:
- SMA vs RP-SMA (check your board!)
- U.FL/IPEX for internal

Like all things Amateur radio you can spend as much $$ as you have here. Or not 😄

----

## Build vs Buy

<div style="font-size:14px">

| Aspect | Buy Ready-Made | Build Your Own |
|--------|----------------|----------------|
| **Setup Time** | ✅ Works out of box | ❌ Time investment |
| **Deployment Speed** | ✅ Faster to deploy | ❌ Slower initial setup |
| **Troubleshooting** | ✅ Less troubleshooting | ❌ Potential issues |
| **Cost** | ❌ More expensive | ✅ Cheaper |
| **Customization** | ❌ Less customization | ✅ Custom features |
| **Learning Experience** | Limited | ✅ Learn more |
| **Best For** | Quick deployment, time-sensitive projects | Hobbyists, custom requirements, budget builds |
| **Note** | Nothing wrong with buying ready-made. Your time has value. | Building is rewarding if you enjoy it. |

</div> 


----

## Where to Buy

<div style="font-size:14px">

**AliExpress**
- Cheapest option
- 2-4 week shipping
- Watch for correct frequency (915 MHz), though can usually be "fixed" with an antenna on SX1262 boards. 
- Check seller ratings

**What to watch for**:
- Correct frequency band (915 MHz for NZ)
- LoRa chip version 
- Included accessories

RAK Equipment should be bought from "RAK Official Store"

Trick on AliExpress, sort your search by "Most Orders"

</div>

----

## Recommended Starter Kit

<div style="font-size:14px">

**Budget Option (~$60 NZD)**:
- RAK 19003 - Smaller RAK board
- Basic stubby antenna
- Panel antennas for 900MHz and Bluetooth
- USB cable

**Complete Option (~$50 USD)**:
- WisMesh Tag
- So-so internal antenna, but great "package deal"
- 1000mAh battery
- GPS/GNSS Receiver
- USB magnetic charger. 

</div>

---

![ctr](https://pad.duckles.nz/uploads/e17ac37f-b592-42d0-8b79-6f8e7a3647e8.png)


---

![ctr](https://pad.duckles.nz/uploads/75e0384e-0f86-449c-9ffc-8660c83e7de4.png)

---



![ctr width:800](https://pad.duckles.nz/uploads/9fb5ac14-383a-475f-9777-906108214d48.png)


---

📷 Repeater Pictures 

---

### v0.0 Maori Hill 
![width:400 ctr](https://pad.duckles.nz/uploads/d4beb86d-4b03-401c-a11c-af5528c42b77.jpeg)

---

| Component | Specification |
|-----------|---------------|
| Enclosure | Weatherized Job Box | 
| Board | RAK |
| Antenna | 3dB AliExpress "special" |
| Battery | 2x 18650 |
| Solar | 3W |

---

### v1.0 Maori Hill and Waihola 

![width:550 ctr](https://pad.duckles.nz/uploads/2c862aef-7243-4486-a73f-0609905b2d06.png)


---

v1.0 Waihola 

![ctr width:800](https://pad.duckles.nz/uploads/665228e9-cc0e-46f5-91e9-14cabcd9f6ac.png)

---

<div class="ctr">

| Component | Specification |
|-----------|---------------|
| Enclosure | AliExpress IP67 150x150x90 Box  | 
| Board | RAK |
| Antenna | 5dB N-Type |
| Battery | 2x 18650 |
| Solar | 10W |
| Solar Charge Controller | AliExpress | 

</div>

----

3-4 weeks on 2x 18650 batteries and no solar input

![ctr width:800](https://pad.duckles.nz/uploads/adb0efe5-75c9-4514-a3a1-f2f779ecd8e4.png)

RAK 4631


---

v0.0 Waihola and Halfway Bush

![ctr width:600](https://pad.duckles.nz/uploads/39444966-7041-4628-971c-dfca97e918f9.png)

---

![ctr](https://pad.duckles.nz/uploads/f5d34f76-6512-406a-8e18-a357898dd31d.png)


---

| Component | Specification |
|-----------|---------------|
| Enclosure | Bunnings Jardin Light | 
| Board | RAK |
| Antenna | 3dB AliExpres |
| Battery | 1x "18650" |
| Solar | 10W |


---

Others - ZL4QC and ZL4MDS 

![width:800 ctr](https://pad.duckles.nz/uploads/45e78d06-5d1c-412e-bd68-a771563f76c5.png)

---

With a bit of 3D printing 
![ctr width:700](https://pad.duckles.nz/uploads/3b3ad46c-d1e5-4135-a142-3104601d2891.png)

[STL](https://makerworld.com/en/models/2327941-50deg-end-cap-for-bunnings-aldi-solar-light?from=search#profileId-2543496)


---

![height:600 ctr](https://pad.duckles.nz/uploads/cc688fa9-b4c8-4e08-9ec9-f7c064002542.png)

---

# Other node ideas 

---

![width:800 ctr](https://pad.duckles.nz/uploads/c95da899-ad8d-4e74-abaf-a2c67b051c0e.png)

Shared by Hio77 in [Discord](https://discord.com/channels/1495203904898728149/1495412712505606315/1498203939043020883)

---

![width:300 ctr](https://pad.duckles.nz/uploads/23d3575f-af13-4eff-9bcd-ccb48dae54d0.png)

Seen on On [NZ regional-channel of meshcore.io Discord](https://discord.com/channels/1495203904898728149/1495412712505606315/1497169474179170415) by jon CLD1


---

![width:300 ctr](https://pad.duckles.nz/uploads/a1e4f1d1-1265-4a16-9518-a63238c3b99d.png)

Seen on On [NZ regional-channel of meshcore.io Discord](https://discord.com/channels/1495203904898728149/1495412712505606315/1497169474179170415) by jon CLD1



---


# Dunedin / Southland Mesh


---

### Region 

![width:800 ctr](https://pad.duckles.nz/uploads/bb926012-8c46-4c8d-b378-8592f627007d.png)


----

### Lower South Island
![width:800 ctr](https://pad.duckles.nz/uploads/72912ff2-045b-4a9c-84f5-b6232d865214.png)


---

### Town
![width:800](https://pad.duckles.nz/uploads/726379e9-c071-4673-8671-6ceb42e79ac8.png)

---

### Waihola and South
![width:800](https://pad.duckles.nz/uploads/4b786ca3-b093-4a29-9e95-69a324c177bf.png)


---

# MeshCore Application

----

## Available Apps

**Mobile**:
- iOS: MeshCore app
- Android: MeshCore app
- Browser: Chrome / Edge (chromium based browser required - no Firefox)
- Connect via USB, Bluetooth or TCP

----

## Coverage Planning in MeshCore App

These tools are in the MeshCore app under "Tools"

**Antenna Coverage**:
- Terrain-aware coverage prediction
- Plan repeater locations

**Line of Sight**:
- Line-of-sight 
- Check LoS between two points


--- 

### Test coverage of a repeater node at Mt. Cargill 

![width:800](https://pad.duckles.nz/uploads/bc99d944-6670-49c7-b7f9-62fe17f04cb7.png)


--- 

### Test Line of Sight from Karatei Rd. to Bull Creek (ZL4UC's crib)

![](https://pad.duckles.nz/uploads/8ab83c14-0567-4d5f-815e-4b38461afb2e.png)


----

## Your First Node

**Step 1**: Choose hardware
- Heltec, RAK, Seed Studio etc. 

**Step 2**: Order from AliExpress
- Verify 915 MHz frequency
- Allow 2-4 weeks shipping

**Step 3**: Flash firmware
- Use web flasher at https://meshcore.io (easiest)

**Step 4**: Configure
- Set your name
- Set region to NZ Narrow
- Post in Public 

---

## Thank You! 




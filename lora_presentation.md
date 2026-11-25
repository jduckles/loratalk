---
marp: true
theme: baleen
size: 16:9
paginate: true
footer: 'LoRa & MeshCore · ZL4EKA · ZL4AA, April 2026'
title: LoRa & MeshCore
description: Mesh networking on the New Zealand lower South Island
author: Jonah Duckles (ZL4EKA)
---

<!-- _class: lead -->
<!-- _footer: '' -->
<!-- _paginate: false -->

![bg right:42% contain](images/whale-tile.svg)

# LoRa & MeshCore

## Mesh networking on the New Zealand lower South Island

**Jonah Duckles** · ZL4EKA
ZL4AA, Dunedin Amateur Radio Club, Branch 30 NZART · 30 April 2026
[jonah@duckles.org](mailto:jonah@duckles.org)

Slides and Python notebooks: [jduckles.github.io/loratalk](https://jduckles.github.io/loratalk)

---

<!-- _class: figure -->

![](images/feynman-quote.jpg)

---

<!-- _class: section -->

![bg right:38%](images/facets-section.svg)

### Part one

# What is LoRa?

---

# LoRa: long range, low power, low data rate

**Lo**ng **Ra**nge wireless communication protocol

<div class="columns">
<div>

- Low power consumption
- Long range: 2 to 10 km urban, 15 to 40 km+ rural
- Lowish bandwidth
- Licence-free ISM bands (we use 915 MHz)
- Perfect for IoT and mesh messaging

</div>
<div>

<div class="stats">
<div class="stat krill"><span>40 km+</span><small>rural range from a few milliwatts</small></div>
</div>

</div>
</div>

---

# Community meshes use LoRa, not LoRaWAN

| LoRa | LoRaWAN |
|------|---------|
| Physical layer | Network protocol |
| Point-to-point | Star topology |
| Peer-to-peer capable | Gateway-based |
| **Community meshes use LoRa** | Commercial IoT |

---

# Why LoRa for mesh?

<div class="columns">
<div>

### Good at

- Works without infrastructure
- A modest battery lasts days or weeks
- Free to use (ISM bands)
- Affordable hardware

</div>
<div>

### Not for

- High-bandwidth applications

</div>
</div>

<div class="callout quiet">

The way we are using it, this is **not** a ham radio mode. Though there are very interesting things going on with APRS LoRa on 70 cm. Stay tuned!

</div>

---

<!-- _class: figure -->

![](figures/rf-landscape.svg)

---

<!-- _class: section -->

![bg right:38%](images/facets-section.svg)

### Part two

# Frequency bands & regulations

---

# NZ gets 915 MHz with no duty-cycle limit

| Region | Frequency | Power limit | Duty cycle |
|--------|-----------|-------------|------------|
| **NZ / AU** | **915 to 928 MHz** | **30 dBm EIRP** | **100%** |
| EU | 868 MHz | 14 dBm | 1 to 10% |
| US | 902 to 928 MHz | 30 dBm | 100% |
| Asia | 433 MHz | Varies | Varies |

<div class="callout">

We're fortunate in NZ to have no duty-cycle restrictions on 915 MHz, unlike Europe. That means better mesh performance. We use the ANZ region settings.

</div>

---

# 30 dBm EIRP is the ceiling, antenna included

**NZ regulations (915 MHz ISM)**

- 30 dBm EIRP maximum
- EIRP = transmit power + antenna gain − cable loss
- EIRP: Effective Isotropic Radiated Power

<div class="stats">
<div class="stat"><span>22 dBm</span><small>transmit (158 mW)</small></div>
<div class="stat"><span>+ 8 dBi</span><small>antenna</small></div>
<div class="stat krill"><span>30 dBm</span><small>EIRP: right at the limit</small></div>
</div>

---

<!-- _class: section -->

![bg right:38%](images/facets-section.svg)

### Part three

# Chirp spread spectrum

---

# What is CSS?

We're trading off sensitivity and data rate while operating in a fixed-bandwidth channel (62.5 to 500 kHz).

**Chirp spread spectrum** is LoRa's secret sauce:

- Frequency "chirps" sweep across the bandwidth
- Data is encoded in chirp timing and frequency
- Extremely noise-resistant
- Can decode signals below the noise floor
- Trade-off: bit rate and speed vs. range vs. reliability

---

<!-- _class: figure -->

![](figures/chirp.svg)

---

![bg contain](https://media1.tenor.com/m/jnkEmKebeKsAAAAd/science-explode.gif)

---

<!-- _class: figure -->

![](figures/three-views.svg)

<!--
Fourier transform: time domain, frequency domain and time-frequency domain.
The original image for this slide was lost with the pad; this chart replaces it.
-->

---

<!-- _class: figure -->

![](figures/sf-tradeoff.gif)

---

<!-- _class: figure -->

![](figures/dechirp.svg)

---

<!-- _class: figure -->

![](figures/noise-resistance.gif)

---

# Recap: spreading buys sensitivity with time

- Spreading factor causes more time on air, so more power use and more processing
- However, SF11's signal-resolving power is 😱
- The magic of signal processing:
  - multiply by a down-chirp to get a constant tone
  - FFT to pull the tones out as symbols
- Spreading factors do not interfere with each other

---

<!-- _class: screenshot compact -->

# A real repeater packet, seen on a waterfall

Packet time runs up the page (earlier is lower), just like a waterfall on your HF rig or SDR. See the preamble, then the chirps.

![h:280](images/sdr-waterfall.png)

<span class="small muted">Captured with SDR++ on a HackRF. Note the LoRa preamble followed by the data chirps.</span>

---

![bg contain](images/meshcore-app.png)

---

![bg contain](https://media1.tenor.com/m/JaS15CLLVo8AAAAC/science.gif)

---

<!-- _class: section -->

![bg right:38%](images/facets-section.svg)

### Part four

# Open mesh network firmwares

---

# Three open firmwares run on the same cheap radios

These are community-developed open source projects. Low-cost, low-power hardware has created a flourishing of software and firmware experimentation.

- [**MeshCore**](https://meshcore.io): the newest kid on the block, designed around Meshtastic's failure modes
- [**Meshtastic**](http://meshtastic.org): been around a bit longer, but has some fundamental design flaws
- [**Reticulum**](https://reticulum.network/): a tool for building networks, including over LoRa

---

# Some MeshCore terms

- **Companion node**: an individual device on the mesh, usually paired over Bluetooth to an app on your phone
- **Repeater**: a fixed node that extends local or regional coverage
- **Room server**: a caching node that saves the last 32 messages for nodes that have been offline
- **Hop**: one message relay between nodes

---

# What happened to Meshtastic?

<div class="columns">
<div>

### Two major flaws

- A flood-always model causing a traffic denial of service
- Internet-connected MQTT further overwhelming airtime

</div>
<div>

### MeshCore learns from them

- Fixed repeaters (don't put a "repeater" in your car... please!)
- Companion nodes
- Room servers
- Observer nodes and more

</div>
</div>

---

# The MeshCore community moved to meshcore.io

The community had a wee schism this last week. It mostly seems to be everyone leaving the person who runs the .co.uk domain in the dust and moving to meshcore.io.

![h:190](https://media1.tenor.com/m/k3uajg33vtYAAAAC/itll-be-totally-fine-elle-evans.gif)

Get involved on the MeshCore.io Discord: https://discord.gg/YGpzsftS

---

# Most of NZ, and now Dunedin, runs SF7

There have been two presets in NZ. SF11 gives better interference resistance and weak-link connections, but much of NZ uses SF7, so the Dunedin community has switched as well.

| Preset | Spreading factor | Channel | Coding rate |
| --- | --- | --- | --- |
| **NZ Narrow** | **7** | **62.5 kHz** | **5** |
| NZ | 11 | 250 kHz | 5 |

<div class="callout quiet">

Talk of switching "NZ Preset" to SF7 / 62.5 kHz as well.

</div>

---

<!-- _class: section -->

![bg right:38%](images/facets-section.svg)

### Part five

# Hardware options

---

# Every LoRa device is a microcontroller plus a radio

- A microcontroller:
  - **ESP32**: higher power consumption (though creative power-management firmwares are closing the gap)
  - **nRF**: much lower power consumption
- An RF board, these days often the [Semtech SX1262](https://semtech.my.salesforce.com/sfc/p/#E0000000JelG/a/RQ000008nKCH/hp2iKwMDKWl34g1D3LBf_zC7TGBRIo2ff5LMnS8r19s)
- Over SPI (Serial Peripheral Interface) you can drive a Semtech board with anything you want

---

<!-- _class: screenshot -->

# Inside the SX1262

![h:400](images/sx1262-block-diagram.png)

---

# The SX1262 is behind the low-cost, low-power boom

<div class="columns">
<div>

- The current recommended chip
- 150 to 960 MHz
- 22 dBm transmit, about 0.154 W
- Longer range potential
- **This is what you want in new hardware right now**

</div>
<div>

<div class="stats">
<div class="stat krill"><span>~5 mA</span><small>receive current, vs ~100 mA</small></div>
<div class="stat"><span>−148</span><small>dBm sensitivity, vs −137 dBm</small></div>
</div>

</div>
</div>

---

# ESP32 or nRF52?

| ESP32-based | nRF52-based |
|-------------|-------------|
| More common | **Lower power (better battery)** |
| Wi-Fi and Bluetooth | Bluetooth only (no Wi-Fi) |
| Cheaper | Fewer options |
| More board options | **Better for solar and portable** |
| Higher power consumption | |

---

<!-- _class: compact -->

# Popular ESP32 boards

| Feature | TTGO T-Beam | Heltec V3 |
|---------|-------------|-----------|
| **GPS** | Included | Not included |
| **Battery** | 18650 battery | Not specified |
| **Display** | OLED display option | Built-in display |
| **Form factor** | Complete package | Compact |
| **Antenna** | Standard connector | Good antenna connector |
| **Price range** | ~$25 to 35 USD | ~$20 to 30 USD |
| **Best use** | Most popular complete solution | Great for portable nodes |

---

# Popular nRF52 boards

### RAK4631 WisBlock

- The most popular nRF option
- Modular: add a screen, sensors or GPS for more cost
- Excellent battery life
- ~$40+ USD

Other nRF options from Seeed Studio and Heltec.

---

# GPS: yes for portable, optional for fixed

<div class="columns">
<div>

### Pros

- Position sharing
- Mapping capabilities
- Time synchronisation
- Useful for mobile nodes

</div>
<div>

### Cons

- Higher power draw
- Not needed for fixed repeaters
- Privacy considerations

</div>
</div>

<div class="callout">

**Recommendation:** yes for portable, optional for fixed (but it can be good for clock sync).

</div>

---

<!-- _class: compact -->

# Display options

| Feature | OLED (0.96" / 1.3") | E-ink | None |
|---------|---------------------|-------|------|
| **Messages, node stats, battery** | Shown | Shown | Phone or computer only |
| **Power consumption** | Standard | Lower | **Lowest** |
| **Sunlight readability** | Standard | **Readable in sunlight** | n/a |
| **Refresh rate** | Fast | Slower | n/a |
| **Cost** | Adds ~$5 to 10 | More expensive | Cheapest |
| **Best use** | General purpose | Outdoor and solar | Budget builds |

---

# Antenna considerations

<div class="columns">
<div>

**Stock antennas** are usually adequate for testing, or around the house and town.

RAK kits come with panel antennas for both 900 MHz and Bluetooth.

### Upgrades

- 3 to 5 dBi: good all-round
- 6+ dBi: fixed repeaters

</div>
<div>

### Connector types

- SMA vs RP-SMA (check your board!)
- U.FL / IPEX for internal

<div class="callout quiet">

Like all things amateur radio, you can spend as much $$ as you have here. Or not 😄

</div>

</div>
</div>

---

<!-- _class: compact -->

# Build or buy: your time has value

| Aspect | Buy ready-made | Build your own |
|--------|----------------|----------------|
| **Setup time** | Works out of the box | Time investment |
| **Troubleshooting** | Less | More potential issues |
| **Cost** | More expensive | Cheaper |
| **Customisation** | Less | Custom features |
| **Learning** | Limited | Learn more |
| **Best for** | Quick deployment | Hobbyists, custom needs, budget builds |

<div class="callout quiet">

Nothing wrong with buying ready-made: your time has value. Building is rewarding if you enjoy it.

</div>

---

<!-- _class: compact -->

# Where to buy

<div class="columns">
<div>

### AliExpress

- Cheapest option
- 2 to 4 week shipping
- Watch for the correct frequency (915 MHz), though on SX1262 boards it can usually be "fixed" with an antenna
- Check seller ratings
- Trick: sort your search by **Most orders**

</div>
<div>

### What to watch for

- Correct frequency band (915 MHz for NZ)
- LoRa chip version
- Included accessories

<div class="callout">

Buy RAK equipment from the **RAK Official Store**.

</div>

</div>
</div>

---

# Recommended starter kits

<div class="columns">
<div>

### Budget (~$60 NZD)

- RAK19003, the smaller RAK board
- Basic stubby antenna
- Panel antennas for 900 MHz and Bluetooth
- USB cable

</div>
<div>

### Complete (~$50 USD)

- WisMesh Tag
- So-so internal antenna, but a great package deal
- 1000 mAh battery
- GPS / GNSS receiver
- USB magnetic charger

</div>
</div>

---

![bg contain](images/starter-kit-board-a.png)
![bg contain](images/starter-kit-board-b.png)

---

![bg contain](images/wismesh-tag.png)

---

<!-- _class: section -->

![bg right:38%](images/facets-section.svg)

### Part six

# Repeater pictures

---

# v0.0 Maori Hill

<div class="columns wide-left">
<div>

![h:400](images/repeater-v0-maori-hill.jpg)

</div>
<div>

| Component | Specification |
|-----------|---------------|
| Enclosure | Weatherised job box |
| Board | RAK |
| Antenna | 3 dB AliExpress "special" |
| Battery | 2× 18650 |
| Solar | 3 W |

</div>
</div>

---

# v1.0 Maori Hill and Waihola

<div class="columns wide-left">
<div>

![h:400](images/repeater-v1-enclosure.jpg)

</div>
<div>

| Component | Specification |
|-----------|---------------|
| Enclosure | AliExpress IP67 150×150×90 box |
| Board | RAK |
| Antenna | 5 dB N-type |
| Battery | 2× 18650 |
| Solar | 10 W |
| Charge controller | AliExpress |

</div>
</div>

---

<!-- _class: screenshot -->

# v1.0 Waihola

![h:400](images/repeater-v1-waihola.jpg)

---

<!-- _class: screenshot compact -->

# 3 to 4 weeks on two 18650s with no solar input

![h:350](images/repeater-battery-no-solar.png)

<span class="small muted">RAK4631</span>

---

<!-- _class: screenshot -->

# v0.0 Waihola and Halfway Bush

![h:400](images/repeater-v0-waihola-halfway-bush.jpg)

---

# The v0.0 build is a Bunnings solar light

<div class="columns wide-left">
<div>

![w:640](images/jardin-solar-light.png)

</div>
<div>

| Component | Specification |
|-----------|---------------|
| Enclosure | Bunnings Jardin light |
| Board | RAK |
| Antenna | 3 dB AliExpress |
| Battery | 1× "18650" |
| Solar | 10 W |

</div>
</div>

---

<!-- _class: screenshot -->

# Others: ZL4QC and ZL4MDS

![h:400](images/zl4qc-zl4mds-solar-lights.png)

---

# With a bit of 3D printing

<div class="columns">
<div>

![h:330](images/3d-printed-end-cap.jpg)

[STL on MakerWorld](https://makerworld.com/en/models/2327941-50deg-end-cap-for-bunnings-aldi-solar-light)

</div>
<div>

![h:400](images/jardin-repeater-mounted.jpg)

</div>
</div>

---

<!-- _class: section -->

![bg right:38%](images/facets-section.svg)

### Part seven

# Other node ideas

---

![bg contain](images/node-idea-hio77.jpg)

<!-- Shared by Hio77 in Discord: https://discord.com/channels/1495203904898728149/1495412712505606315/1498203939043020883 -->

---

![bg contain](images/node-idea-cld1-a.jpg)
![bg contain](images/node-idea-cld1-b.jpg)

<!-- Seen on the NZ regional channel of the meshcore.io Discord, by jon CLD1: https://discord.com/channels/1495203904898728149/1495412712505606315/1497169474179170415 -->

---

<!-- _class: section -->

![bg right:38%](images/facets-section.svg)

### Part eight

# Dunedin / Southland mesh

---

<!-- _class: screenshot -->

# Region

![h:400](images/map-region.jpg)

---

<!-- _class: screenshot -->

# Lower South Island

![h:400](images/map-lower-south-island.jpg)

---

<!-- _class: screenshot -->

# Town

![h:400](images/map-town.jpg)

---

# Maori Hill repeater view

Sitting at 48% battery 😬

<div class="callout warn">

**Missing image.** This screenshot lived only on the HedgeDoc pad and wasn't in the April 29 PDF, so it couldn't be recovered. Drop it in as `images/maori-hill-repeater-view.png`.

</div>

---

<!-- _class: screenshot -->

# Waihola and south

![h:400](images/map-waihola-south.jpg)

---

# One more map

<div class="callout warn">

**Missing image.** The map after "Waihola and south" lived only on the HedgeDoc pad and couldn't be recovered. Drop it in as `images/map-south.png`, or cut this slide.

</div>

---

<!-- _class: section -->

![bg right:38%](images/facets-section.svg)

### Part nine

# The MeshCore app

---

# One app on phone, browser or desktop

### Mobile

- iOS: MeshCore app
- Android: MeshCore app

### Browser

- Chrome or Edge (a Chromium-based browser is required; no Firefox)
- Connect over USB, Bluetooth or TCP

---

# Plan coverage before you climb the hill

These tools are in the MeshCore app under **Tools**.

<div class="columns">
<div>

### Antenna coverage

- Terrain-aware coverage prediction
- Plan repeater locations

</div>
<div>

### Line of sight

- Check line of sight between two points

</div>
</div>

---

<!-- _class: screenshot -->

# Test coverage of a repeater node at Mt Cargill

![h:400](images/coverage-mt-cargill.jpg)

---

<!-- _class: screenshot compact -->

# Test line of sight from Karatei Rd to Bull Creek (ZL4UC's crib)

![h:400](images/line-of-sight-bull-creek.jpg)

---

# Your first node, in four steps

<div class="columns">
<div>

1. **Choose hardware**: Heltec, RAK, Seeed Studio etc.
2. **Order from AliExpress**: verify 915 MHz, allow 2 to 4 weeks

</div>
<div>

3. **Flash firmware**: the web flasher at [meshcore.io](https://meshcore.io) is easiest
4. **Configure**: set your name, set the region to **NZ Narrow**, post in Public

</div>
</div>

---

<!-- _class: lead -->
<!-- _footer: '' -->
<!-- _paginate: false -->

![bg right:42% contain](images/whale-tile.svg)

# Thank you!

## Questions?

[jduckles.github.io/loratalk](https://jduckles.github.io/loratalk/)

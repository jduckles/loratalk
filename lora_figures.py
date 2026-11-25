"""The LoRa talk's figures, drawn in baleen (jduckles/visual).

Every plot in the deck that came from Python is rebuilt here from the two
notebooks' code, so the images live in the repo and can't be lost again.

    python lora_figures.py            # writes figures/*.svg|png|gif

Or from a notebook, change a parameter and redraw one figure:

    import lora_figures as lf
    lf.noise_resistance(snr_db=-20)

The signal maths is the notebooks' own (generate_upchirp, generate_downchirp,
add_noise, dechirp_and_fft). Only the drawing changed.
"""
from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import baleen.mpl as bm

OUT = Path(__file__).parent / "figures"
SF_VALUES = [7, 8, 9, 10, 11, 12]
SOURCE = "loratalk notebooks, simulated LoRa chirps"


# ------------------------------------------------------------ signal maths (from the notebooks)

def generate_upchirp(SF, BW, fs, symbol_value=0):
    M = 2**SF
    Ts = M / BW
    N = int(fs * Ts)
    t = np.linspace(0, Ts, N, endpoint=False)
    f0 = -BW / 2
    k = BW / Ts
    shift = symbol_value / M
    upchirp = np.exp(1j * 2 * np.pi * (f0 * t + 0.5 * k * t**2 + shift * BW * t))
    return upchirp, t, Ts, N


def generate_downchirp(SF, BW, fs):
    M = 2**SF
    Ts = M / BW
    N = int(fs * Ts)
    t = np.linspace(0, Ts, N, endpoint=False)
    f0 = BW / 2
    k = -BW / Ts
    return np.exp(1j * 2 * np.pi * (f0 * t + 0.5 * k * t**2))


def add_noise(signal, snr_db, rng):
    signal_power = np.mean(np.abs(signal)**2)
    noise_power = signal_power / 10**(snr_db / 10)
    noise = np.sqrt(noise_power / 2) * (rng.standard_normal(len(signal))
                                        + 1j * rng.standard_normal(len(signal)))
    return signal + noise, noise


def dechirp_and_fft(signal, downchirp):
    return np.abs(np.fft.fft(signal * downchirp))


def spectrogram(sig, fs, nfft=64, step=4):
    """Short-time power in dB: (times_s, freqs_hz, power_db), frequencies centred on 0."""
    win = np.hanning(nfft)
    starts = np.arange(0, max(len(sig) - nfft, 1), step)
    frames = np.stack([sig[s:s + nfft] * win for s in starts]) if len(sig) >= nfft else \
        np.zeros((1, nfft), complex)
    P = np.abs(np.fft.fftshift(np.fft.fft(frames, axis=1), axes=1))**2
    f = np.fft.fftshift(np.fft.fftfreq(nfft, 1 / fs))
    t = (starts + nfft / 2) / fs
    return t, f, 10 * np.log10(P.T + 1e-10)


# ------------------------------------------------------------ helpers

def _seq():
    return f"baleen_seq_{bm.M().name}"


def _quiet(ax):
    """A panel that is a picture (spectrogram, waveform), not a bar chart: no grid."""
    ax.grid(False)


def _panel_title(ax, text):
    ax.set_title(text, loc="left", fontsize=bm.S()["text"], fontweight=600, color=bm.M().ink,
                 pad=6)


def _frames_to_gif(frames, path, ms):
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=ms, loop=0,
                   optimize=True, disposal=2)
    return path


def _grab(fig, dpi=110):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT,
                                                   dither=Image.Dither.NONE)


# ------------------------------------------------------------ 1. what a chirp looks like

def chirp(mode="light", out=OUT):
    """A chirp is a tone that slides up in frequency. Replaces the paper's 'Figure 5'."""
    bm.use(mode, "slide")
    fig, (ax, axf) = bm.figure(nrows=2, hspace=0.55)
    fig.axes[0].get_gridspec().set_height_ratios([2.2, 1])
    t = np.linspace(0, 5, 6000)
    f = 0.25 + 1.4 * t                       # frequency rises linearly with time
    phase = 2 * np.pi * (0.25 * t + 0.7 * t**2)
    ax.plot(t, np.sin(phase), color=bm.hue("tide"), lw=1.6)
    ax.set_xlim(0, 5)
    ax.set_ylim(-1.3, 2.25)
    ax.set_yticks([-1, 0, 1])
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    bm.unit(ax, "Amplitude")
    bm.callout(ax, (0.42, 1.0), "Starts slow", "low frequency, wide waves", at=(0.75, 1.45),
               color=bm.hue("tide"))
    bm.callout(ax, (4.62, 1.0), "Ends fast", "same amplitude, higher frequency",
               at=(4.3, 1.45), color=bm.hue("tide"), ha="right")
    axf.plot(t, f, color=bm.M().emphasis, lw=2.4)
    axf.set_xlim(0, 5)
    axf.set_ylim(0, 8)
    axf.set_yticks([0, 4, 8])
    axf.set_xticks(range(6))
    axf.set_xticklabels([])
    axf.text(5, 0.3, "time", ha="right", va="bottom", fontsize=bm.S()["label"],
             color=bm.M().muted, fontweight=600)
    bm.unit(axf, "Frequency")
    axf.text(2.5, 5.2, "the frequency climbs in a straight line: that is the chirp",
             ha="center", fontsize=bm.S()["text"], color=bm.M().ink, fontweight=600)
    bm.title(fig, "A chirp is one tone sliding steadily up in frequency",
             "LoRa sends every symbol as a chirp that sweeps across the channel")
    bm.brand(fig, source="illustration, after Semtech's chirp spread spectrum figure")
    return bm.save(fig, out / "chirp")


# ------------------------------------------------------------ 2. the same chirp three ways

def three_views(mode="light", out=OUT, BW=125e3, Ts=1e-3):
    """Time, frequency and time-frequency views of one chirp (the Fourier slide).

    Drawn as a chirp sweeping 0 to BW so its wiggles visibly speed up; LoRa's own
    chirps sweep -BW/2 to +BW/2 around the carrier, which is the same shape.
    """
    bm.use(mode, "slide")
    fs = 8 * BW
    t = np.arange(int(fs * Ts)) / fs
    up = np.exp(1j * 2 * np.pi * (0.5 * BW / Ts * t**2))
    N = len(t)
    fig, axes = bm.figure(ncols=3, wspace=0.22)
    a1, a2, a3 = axes
    tt = np.linspace(0, Ts, 20000)
    a1.plot(tt * 1e3, np.cos(2 * np.pi * 0.5 * 30e3 / Ts * tt**2), color=bm.hue("tide"),
            lw=1.1)
    a1.set_xlim(0, Ts * 1e3)
    a1.set_ylim(-1.2, 1.2)
    a1.set_yticks([])
    a1.set_xticks([0, 0.5, 1])
    a1.xaxis.set_major_formatter(lambda v, _: f"{v:g}")
    _quiet(a1)
    _panel_title(a1, "Time: a wiggle that speeds up (drawn slower)")
    spec = np.abs(np.fft.fft(up))
    fr = np.fft.fftfreq(N, 1 / fs) / 1e3
    o = np.argsort(fr)
    fr, spec = fr[o], spec[o] / spec.max()
    a2.fill_between(fr, 0, spec, color=bm.wash("tide"), lw=0)
    a2.plot(fr, spec, color=bm.hue("tide"), lw=1.2)
    a2.set_xlim(-30, BW / 1e3 + 30)
    a2.set_ylim(0, 1.3)
    a2.set_yticks([])
    a2.set_xticks([0, 62.5, 125])
    a2.xaxis.set_major_formatter(lambda v, _: f"{v:g}")
    _panel_title(a2, "Frequency (kHz): a flat block")
    a2.text(BW / 2e3, 1.14, "every frequency, but not when", ha="center",
            fontsize=bm.S()["note"], color=bm.M().muted)
    st, sf, sp = spectrogram(np.concatenate([np.zeros(128), up, np.zeros(128)]), fs,
                             nfft=256, step=4)
    st = st - 128 / fs
    keep = (sf >= -10e3) & (sf <= BW + 10e3)
    a3.pcolormesh(st * 1e3, sf[keep] / 1e3, sp[keep], cmap=_seq(), shading="auto", rasterized=True,
                  vmin=sp.max() - 30, vmax=sp.max())
    a3.set_xlim(0, Ts * 1e3)
    a3.set_ylim(-10, BW / 1e3 + 10)
    a3.set_yticks([0, 62.5, 125])
    a3.yaxis.set_major_formatter(lambda v, _: f"{v:g}")
    a3.set_xticks([0, 0.5, 1])
    a3.xaxis.set_major_formatter(lambda v, _: f"{v:g}")
    _quiet(a3)
    _panel_title(a3, "Time (ms) and frequency: a diagonal line")
    bm.title(fig, "Only the time-frequency view shows what a chirp is",
             f"One chirp sweeping a {BW/1e3:.0f} kHz channel in 1 ms, seen three ways")
    bm.brand(fig, source="loratalk, simulated chirp")
    return bm.save(fig, out / "three-views")


# ------------------------------------------------------------ 3. spreading factor vs time on air

def _sf_frame(SF, BW, fs, fixed_time, mode):
    bm.use(mode, "slide")
    fig, axes = bm.figure(nrows=3, hspace=0.75)
    a1, a2, a3 = axes
    up, t, Ts, N = generate_upchirp(SF, BW, fs)
    total = int(fs * fixed_time)
    sig = np.zeros(total, complex)
    sig[:len(up)] = up
    tt = np.arange(total) / fs * 1e3
    rate = SF * BW / 2**SF

    a1.axvspan(0, Ts * 1e3, color=bm.wash("krill"), lw=0, zorder=0)
    a1.plot(tt, sig.real, color=bm.hue("tide"), lw=0.6, rasterized=True)
    a1.axvline(Ts * 1e3, color=bm.M().emphasis, lw=1.6, dashes=(4, 3))
    a1.text(Ts * 1e3 + 0.25, 1.05, f"symbol ends at {Ts*1e3:.2f} ms", fontsize=bm.S()["note"],
            fontweight=600, color=bm.M().emphasis, va="bottom")
    a1.set_xlim(0, fixed_time * 1e3)
    a1.set_ylim(-1.25, 1.25)
    a1.set_yticks([])
    _quiet(a1)
    _panel_title(a1, "The chirp in time")

    st, sf, sp = spectrogram(sig, fs, nfft=64, step=4)
    a2.pcolormesh(st * 1e3, sf / 1e3, sp, cmap=_seq(), shading="auto", rasterized=True,
                  vmin=sp.max() - 35, vmax=sp.max())
    a2.axvline(Ts * 1e3, color=bm.M().emphasis, lw=1.6, dashes=(4, 3))
    a2.set_xlim(0, fixed_time * 1e3)
    a2.set_ylim(-BW / 2e3, BW / 2e3)
    a2.set_yticks([-50, 0, 50])
    _quiet(a2)
    _panel_title(a2, "The same chirp sweeping the channel (kHz)")
    a2.set_xticks(range(0, int(fixed_time * 1e3) + 1, 5))
    a2.xaxis.set_major_formatter(lambda v, _: f"{v:.0f} ms" if v == 35 else f"{v:.0f}")

    times = [2**s / BW * 1e3 for s in SF_VALUES]
    cols = [bm.M().emphasis if s == SF else bm.M().context for s in SF_VALUES]
    bars = a3.barh([f"SF{s}" for s in SF_VALUES], times, color=cols, height=0.66)
    a3.invert_yaxis()
    a3.set_xlim(0, fixed_time * 1e3)
    a3.grid(axis="y", visible=False)
    a3.grid(axis="x", visible=True)
    a3.tick_params(axis="y", labelsize=bm.S()["label"])
    for b, v, s in zip(bars, times, SF_VALUES):
        a3.text(v + 0.3, b.get_y() + b.get_height() / 2, f"{v:.2f} ms",
                va="center", fontsize=bm.S()["note"],
                fontweight=700 if s == SF else 400,
                color=bm.M().ink if s == SF else bm.M().muted)
    _panel_title(a3, "Time on air for one symbol (ms)")
    a3.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}")
    bm.title(fig, "Each step up in spreading factor doubles the time on air",
             f"SF{SF}: {Ts*1e3:.2f} ms per symbol, {rate:,.0f} bits per second "
             f"in a {BW/1e3:.0f} kHz channel")
    bm.brand(fig, source=SOURCE)
    return fig


def sf_tradeoff(mode="light", out=OUT, BW=125e3, fixed_time=0.035):
    """Animated: SF7 to SF12, one frame each (spreading_factor.ipynb). Also a still at SF9."""
    fs = 2 * BW
    frames = [_grab(_sf_frame(sf, BW, fs, fixed_time, mode)) for sf in SF_VALUES]
    gif = _frames_to_gif(frames, out / "sf-tradeoff.gif", 1400)
    still = bm.save(_sf_frame(9, BW, fs, fixed_time, mode), out / "sf-tradeoff")
    plt.close("all")
    return [gif, *still]


# ------------------------------------------------------------ 4. dechirp and FFT: how symbols come back

def dechirp(mode="light", out=OUT, SF=7, BW=125e3, symbols=(12, 67, 3, 98, 45, 120, 31, 77)):
    """Eight chirps in, eight numbers out. Rebuilt from the deck's three-panel figure."""
    bm.use(mode, "slide")
    M = 2**SF
    Ts = M / BW
    fs = BW                         # one sample per chip: FFT bin == symbol value
    down = generate_downchirp(SF, BW, fs)
    fig, axes = bm.figure(nrows=3, hspace=0.85)
    a1, a2, a3 = axes
    tick = bm.M().context
    for i, s in enumerate(symbols):
        t0 = i * Ts * 1e3
        tt = np.linspace(0, Ts, 400, endpoint=False)
        f = (-BW / 2 + s / M * BW + BW / Ts * tt)
        f = (f + BW / 2) % BW - BW / 2               # wraps at the top of the channel
        brk = np.where(np.diff(f) < 0)[0]
        ff = f.copy() / 1e3
        if len(brk):
            ff[brk[0] + 1] = np.nan
        a1.plot(t0 + tt * 1e3, ff, color=bm.hue("tide"), lw=1.8)
        a1.text(t0 + Ts * 1e3 / 2, BW / 2e3 + 8, str(s), ha="center", va="bottom",
                fontsize=bm.S()["note"], fontweight=700, color=bm.M().ink)
        tone = s / M * BW / 1e3
        a2.plot([t0, t0 + Ts * 1e3], [tone, tone], color=bm.hue("tide"), lw=2.6,
                solid_capstyle="butt")
        a2.text(t0 + Ts * 1e3 / 2, tone + 9, str(s), ha="center", va="bottom",
                fontsize=bm.S()["note"], fontweight=700, color=bm.M().ink)
        for a in (a1, a2):
            a.axvline(t0, color=tick, lw=0.8, dashes=(2, 3), zorder=0)
    for a in (a1, a2):
        a.set_xlim(-0.1, len(symbols) * Ts * 1e3 + 0.1)
        _quiet(a)
        a.set_xticks(range(0, 9, 2))
        a.xaxis.set_major_formatter(lambda v, _: f"{v:.0f} ms" if v == 8 else f"{v:.0f}")
    a1.set_ylim(-BW / 2e3 - 6, BW / 2e3 + 30)
    a1.set_yticks([-50, 0, 50])
    _panel_title(a1, "1  Sent: eight chirps, each starting at a different frequency (kHz)")
    a2.set_ylim(-5, BW / 1e3 + 25)
    a2.set_yticks([0, 50, 100])
    _panel_title(a2, "2  Multiplied by a down-chirp: each becomes one steady tone (kHz)")

    rx = np.concatenate([generate_upchirp(SF, BW, fs, s)[0] for s in symbols])
    got = []
    for i in range(len(symbols)):
        spec = dechirp_and_fft(rx[i * M:(i + 1) * M], down)
        got.append(int(np.argmax(spec)))
        a3.vlines(got[-1], 0, 1, color=bm.M().emphasis, lw=2.2)
        a3.plot(got[-1], 1, "o", ms=9, mfc=bm.M().emphasis, mec=bm.M().paper, mew=1.6)
        a3.text(got[-1], 1.12, str(got[-1]), ha="center", va="bottom",
                fontsize=bm.S()["note"], fontweight=700, color=bm.M().ink)
    a3.set_xlim(0, M)
    a3.set_ylim(0, 1.45)
    a3.set_yticks([])
    a3.set_xticks([0, 32, 64, 96, 128])
    _panel_title(a3, "3  FFT of each tone: the peak's bin (0 to 127) is the symbol")
    bm.title(fig, "Dechirp, then FFT: every chirp comes back as a number",
             f"Recovered {got} from {len(symbols)} SF{SF} chirps, {BW/1e3:.0f} kHz channel")
    bm.brand(fig, source=SOURCE)
    assert got == list(symbols), got
    return bm.save(fig, out / "dechirp")


# ------------------------------------------------------------ 5. processing gain beats the noise

def _noise_frame(SF, BW, fs, snr_db, rng, mode):
    bm.use(mode, "slide")
    fig, axes = bm.figure(nrows=3, ncols=2, hspace=0.95, wspace=0.16)
    (a1, a2), (a3, a4), (a5, a6) = axes
    M = 2**SF
    max_Ts = 2**12 / BW
    up, t, Ts, N = generate_upchirp(SF, BW, fs, M // 4)
    down = generate_downchirp(SF, BW, fs)
    noisy, noise = add_noise(up, snr_db, rng)
    gain = 10 * np.log10(M)
    eff = snr_db + gain
    t_ms = t * 1e3

    for a, y, col, ttl, lw in ((a1, up.real, bm.hue("tide"), "Clean chirp", 0.5),
                               (a2, noisy.real, bm.M().context, f"What arrives: chirp + noise at {snr_db} dB SNR", 0.3)):
        a.axvspan(0, Ts * 1e3, color=bm.wash("tide"), lw=0, zorder=0)
        a.plot(t_ms, y, color=col, lw=lw, rasterized=True)
        a.set_xlim(0, max_Ts * 1e3)
        a.set_yticks([])
        _quiet(a)
        _panel_title(a, ttl)
        a.xaxis.set_major_formatter(lambda v, _: f"{v:.0f} ms" if v == 30 else f"{v:.0f}")
    a1.set_ylim(-1.5, 1.5)
    a2.set_ylim(-8, 8)

    max_N = int(fs * max_Ts)
    pad_clean = np.zeros(max_N, complex)
    pad_clean[:N] = up
    pad_noisy = np.sqrt(np.mean(np.abs(noise)**2) / 2) * (rng.standard_normal(max_N)
                                                          + 1j * rng.standard_normal(max_N))
    pad_noisy[:N] = noisy
    for a, sig, ttl in ((a3, pad_clean, "Clean, in time and frequency"),
                        (a4, pad_noisy, "Noisy: the chirp is invisible to the eye")):
        st, sfq, sp = spectrogram(sig, fs, 64, 4)
        a.pcolormesh(st * 1e3, sfq / 1e3, sp, cmap=_seq(), shading="auto", rasterized=True,
                     vmin=sp.max() - 35, vmax=sp.max())
        a.set_xlim(0, max_Ts * 1e3)
        a.set_ylim(-BW / 2e3, BW / 2e3)
        a.set_yticks([-50, 0, 50])
        _quiet(a)
        _panel_title(a, ttl)
        a.xaxis.set_major_formatter(lambda v, _: f"{v:.0f} ms" if v == 30 else f"{v:.0f}")
    a4.set_yticklabels([])

    clean_fft = dechirp_and_fft(up, down)
    noisy_fft = dechirp_and_fft(noisy, down)
    clean_n, noisy_n = clean_fft / clean_fft.max(), noisy_fft / noisy_fft.max()
    half = len(noisy_n) // 2
    peak = int(np.argmax(noisy_n[:half]))
    mask = np.ones(half, bool)
    mask[max(0, peak - 15):min(half, peak + 15)] = False
    floor = noisy_n[:half][mask].mean()
    zw = int(half * 0.5)
    lo, hi = max(0, peak - zw // 2), min(half, peak + zw // 2)
    bins = np.arange(lo, hi)
    a5.plot(bins, noisy_n[lo:hi], color=bm.M().context, lw=0.9)
    a5.axhline(floor, color=bm.hue("tide"), lw=1.2, dashes=(4, 3))
    a5.text(hi, floor + 0.04, "noise floor", ha="right", va="bottom",
            fontsize=bm.S()["note"], fontweight=600, color=bm.hue("tide"))
    a5.plot(peak, noisy_n[peak], "o", ms=10, mfc=bm.M().emphasis, mec=bm.M().paper, mew=1.6,
            zorder=5)
    a5.text(peak + (hi - lo) * 0.03, noisy_n[peak], f"the symbol, bin {peak}",
            va="center", fontsize=bm.S()["note"], fontweight=700, color=bm.M().ink)
    a5.set_xlim(lo, hi)
    a5.set_ylim(0, 1.35)
    a5.set_yticks([])
    _panel_title(a5, "After dechirp + FFT: one peak stands clear")

    gains = [10 * np.log10(2**s) for s in SF_VALUES]
    cols = [bm.M().emphasis if s == SF else bm.M().context for s in SF_VALUES]
    bars = a6.bar([f"SF{s}" for s in SF_VALUES], gains, color=cols, width=0.66)
    a6.axhline(-snr_db, color=bm.hue("tide"), lw=1.2, dashes=(4, 3))
    a6.text(-0.4, 46, f"dashed line: the {-snr_db} dB needed to climb out of the noise",
            fontsize=bm.S()["note"], fontweight=600, color=bm.hue("tide"), va="top")
    for b, g, s in zip(bars, gains, SF_VALUES):
        a6.text(b.get_x() + b.get_width() / 2, g + 0.8, f"{g:.0f}", ha="center", va="bottom",
                fontsize=bm.S()["note"], fontweight=700 if s == SF else 400,
                color=bm.M().ink if s == SF else bm.M().muted)
    a6.set_ylim(0, 50)
    a6.set_yticks([0, 20, 40])
    a6.tick_params(axis="x", labelsize=bm.S()["label"])
    _panel_title(a6, "Processing gain (dB) by spreading factor")
    bm.title(fig, "Spreading lets LoRa hear a signal buried under the noise",
             f"SF{SF}: {gain:.1f} dB of processing gain turns {snr_db} dB SNR into "
             f"{eff:+.1f} dB at the decoder")
    bm.brand(fig, source=SOURCE + " (simplified model: gain = 10·log10(2^SF))")
    return fig


def noise_resistance(mode="light", out=OUT, BW=125e3, snr_db=-15, seed=42):
    """Animated: SF7 to SF12 (gain_from_spreading_factor.ipynb). Also a still at SF7."""
    fs = 2 * BW
    rng = np.random.default_rng(seed)
    frames = [_grab(_noise_frame(sf, BW, fs, snr_db, rng, mode)) for sf in SF_VALUES]
    gif = _frames_to_gif(frames, out / "noise-resistance.gif", 2200)
    still = bm.save(_noise_frame(7, BW, fs, snr_db, np.random.default_rng(seed), mode),
                    out / "noise-resistance")
    plt.close("all")
    return [gif, *still]


# ------------------------------------------------------------ 6. where LoRa sits among radios

def rf_landscape(mode="light", out=OUT):
    """The 'LoRa's place in the modern world of RF' slide as a baleen diagram."""
    from baleen.svg import Sheet
    s = Sheet(1200, 675, mode=mode, title="LoRa trades data rate for range, battery and cost",
              subtitle="Six families of IoT radio, by what each is good and bad at",
              source="after Semtech, 'IoT Technologies' (Figure 1)",
              alt="Six radio families in a grid. LPWAN (LoRa) in the centre: long range, low "
                  "data rates, long battery life, low cost.")
    W, H = s.body_w, s.body_h
    gap = 22
    cw = (W - 2 * gap) / 3
    rh = (H - gap) / 2
    cells = [
        (0, 0, "context", "Traditional cellular", None, ["Long range", "High data rates",
                                                           "Low battery life", "High cost"], "antenna"),
        (1, 0, "krill", "LPWAN: LoRa", "the one we use", ["Long range", "Low data rates",
                                                           "Long battery life", "Low cost"], "ripple"),
        (2, 0, "context", "Cat-M1", "LTE for devices", ["Long range", "High data rates",
                                                         "Low battery life", "Medium cost"], "antenna"),
        (0, 1, "context", "Local area network", "Wi-Fi", ["Short range", "High data rates",
                                                           "Low battery life", "Medium cost"], "router"),
        (1, 1, "context", "Narrow-band IoT", "NB-IoT", ["Short range, indoors", "Low data rates",
                                                         "Good battery life", "Low cost"], "building"),
        (2, 1, "context", "Personal area network", "Bluetooth", ["Very short range", "Low data rates",
                                                                  "Good battery life", "Low cost"], "device-mobile"),
    ]
    for c, r, hue, head, label, lines, icon in cells:
        x, y = c * (cw + gap), r * (rh + gap)
        if hue == "krill":
            s.region(x, y, cw, rh, "krill", head, lines, icon=icon, label=label, size=18)
        else:
            s.region(x, y, cw, rh, "context", head, lines, icon=icon, label=label, size=18)
    return s.save(out / "rf-landscape")


ALL = (chirp, three_views, sf_tradeoff, dechirp, noise_resistance, rf_landscape)

if __name__ == "__main__":
    import sys
    names = sys.argv[1:]
    for fn in ALL:
        if not names or fn.__name__ in names:
            for p in fn():
                print(p)

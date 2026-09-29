# Slide 1: Beyond Human Sight — Decoding Earth through Radiative Transfer

Good morning, respected committee members and faculty.

We are creating a thing that understands the language of radiative transfer plus optical physics like no human mentally can or was physically designed to understand. As human beings, our vision is confined to only a razor-thin 300-nanometer slice of visible light: Red, Green, and Blue. And what we cannot see, we cannot understand.

Every day, 140 million Indian smallholders look at their crops through these limited RGB eyes. But nature does not speak in RGB. The true biochemical language of Earth — cellular water stress, nitrogen deficiency, leaf carotenoids, and soil sodicity — is written across 400 to 2,500 nanometers of continuous reflected solar radiation.

This thing we are engineering — call it an AI foundation model, a deep learning architecture, or a physics-informed neural operator — bridges that perceptual chasm. This is BharatSpectral: Democratized Spectral-Semantic Intelligence (DSSI).

# Slide 2: Project Objectives — Capstone 7th Semester Scope

Having established why RGB perception fails on Indian smallholder ecosystems, our work is governed by six rigorous, interconnected action objectives:

1. Data Acquisition and Benchmark Creation: We ingest heterogeneous hyperspectral cubes across AVIRIS-NG India (425 bands), ISRO HysIS (220 bands), and NASA EMIT (285 bands) to construct BharatHSI-Bench — India's first open, labeled smallholder agricultural benchmark with standardized evaluation protocols.

2. Empirical Failure Proof: We evaluate global foundation models like SpectralGPT and HyperSIGMA directly on BharatHSI-Bench, quantifying severe domain-shift degradation — a 15% to 30% Overall Accuracy drop caused by fragmented Indian farm plots and multi-crop intercropping.

3. Physics-Informed Foundation Model: We pre-train BharatSpectral-MAE, incorporating seven named architectural innovations — SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, and FASU — enforcing radiative transfer directly inside the Transformer.

4. Comprehensive Evaluation and Ablation: We benchmark against state-of-the-art architectures and conduct systematic ablations to isolate the exact empirical gain of each physical module.

5. Model Distillation for Edge Inference: We compress foundation representations into lightweight ONNX student models, achieving sub-second Serverless Spectral Inference (SSI) within strict memory and compute bounds.

6. Democratized WebGIS Public Infrastructure: We deploy the inference engine into an open, zero-egress public WebGIS platform on Cloudflare R2, Workers, and MapLibre GL JS, delivering biochemical spectral intelligence directly to farmers at zero end-user cost.

# Slide 3: The Web of Fields — Interdisciplinary Convergence

This work converges at the nexus of distinct disciplines:

Optical Physics and Radiative Transfer provide the governing laws so the model adheres to molecular reality;

Deep Learning and 3D Transformers provide the scale to learn from massive unlabeled data;

And Digital Public Infrastructure enables sovereign, zero-cost societal delivery for 140 million Indian smallholders.

# Slide 4: Continuous Spectroscopy — What Each Spectral Band Captures

To see why hyperspectral is revolutionary, look at continuous spectroscopy: while multispectral satellites like Sentinel-2 sample only 10 to 12 broad bands, BharatSpectral resolves 425 continuous narrow channels.

This captures exact biochemical absorption dips: chlorophyll pigments, red-edge cellular inflection, canopy moisture at 970 nanometers, and organic nitrogen and soil organic carbon in the shortwave infrared.

# Slide 5: The "Pinball Machine" Physics — Non-Linear Scattering & 3D Pixels

In smallholder fields, sunlight undergoes a "photon pinball machine" — scattering non-linearly across intercropped canopies, soil, and moisture. Every pixel in our 3D data cube is a continuous physical spectrum, not an RGB color. Traditional linear GIS tools fail here, necessitating our physics-grounded foundation model.

To walk us through the Indian corpus and our data pipeline, I pass to my teammate.

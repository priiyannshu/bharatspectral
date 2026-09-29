# Slide 6: Open Hyperspectral Corpus over the Indian Landmass

Thank you. To build Democratized Spectral-Semantic Intelligence (DSSI), the very first requirement is clean, ground-truth data over real Indian terrain. That is what Phase 1 delivers.

As you see on this coverage map, we have completed Phase 1 by curating India’s first open 1.2-terabyte hyperspectral corpus, harmonizing three distinct sources:

1. High-resolution airborne flights from AVIRIS-NG India over agricultural tracts in Gujarat, Andhra Pradesh, and Punjab;

2. Satellite sweeps from ISRO HysIS;

3. And space station observations from NASA EMIT.

This gives our AI both wide geographic coverage and ultra-detailed spectral resolution, capturing subtle soil and crop chemistry across the Indian landmass.

# Slide 7: Preprocessing & Physical Normalization Pipeline

Raw hyperspectral data from space is essentially a noisy binary dump distorted by the atmosphere, sensor angles, and water vapor. Slide 7 shows our clean 4-step pipeline that transforms raw feeds into standardized, analysis-ready data cubes:

First, we strip away atmospheric haze using radiative physics, converting raw numbers into true surface reflectance.

Second, we prune out unusable atmospheric water noise, distilling 400+ messy bands into 200 standardized, reliable channels.

Third, we slice continuous flight swaths into uniform 3D cubes for model training.

And fourth, we store them in a modern, cloud-native storage format. This step is critical: it is not just a static archive for training, but a live ingestion pipeline. Whenever new satellite data flows into our system in the future, it is automatically cleaned and formatted for instant AI inference.

# Slide 8: Benchmarking Previous Attempts: Empirical Proof of Need

With clean data in place, Phase 2 was about answering a critical question: Can we just use existing computer vision or standard machine learning models?

The answer is a definitive no. As shown in our benchmark table and the bar chart, when we evaluated five leading architectures on our testbed, every single one suffered a severe collapse — dropping between 22% and 37% in accuracy.

We call this "The Indian Pines Fallacy." For 30 years, researchers have benchmarked hyperspectral AI on a 1992 dataset from Indiana in the US, which consists of massive 40-hectare monoculture corn fields.

Indian agriculture is the exact opposite: smallholder farms average just one hectare, multiple crops are grown together in the same plot, and crop cycles shift across three seasons. Western models fail here because they lack physical grounding.

# Slide 9: Why Existing Methods Fail in Indian Smallholder Ecosystems

So why not rely on traditional GIS software like ENVI or QGIS?

Looking at our diagnostic figure on the left, the issue becomes immediately clear. Traditional GIS tools like the Spectral Angle Mapper only compare the angular shape of a spectral curve, completely ignoring its brightness magnitude. In simple terms: a healthy leaf in the shade looks almost identical to a diseased leaf in bright sun. The tool is blind to that difference, resulting in a 36% false alert rate.

Similarly, traditional GIS linear unmixing assumes farm fields are flat paint chips, ignoring how light bounces inside 3D crop canopies.

Traditional GIS tools are too rigid, while standard AI models are too brittle. BharatSpectral bridges both worlds — injecting spectroscopic physics directly into modern Transformers to create DSSI.

To show how our Phase 3 architecture achieves this, I will now hand over to Member 3.

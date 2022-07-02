# DreamCoder Compression Benchmark

This set of benchmarks aims to provide snapshots of the intermediate sets of programs processed by DreamCoder's compressor, so that compression can be studied and innovated on with realistic synthetic programs, without the expensive search involved in running the full DreamCoder pipeline.

We have extracted the top-5 programs from each task sent to the DreamCoder compressor during each iteration of compression in which at least one new invention was added to the library. We do this for 27 DreamCoder runs spanning over 6 domains. We also record which inventions were discovered by DreamCoder.

Note that we can only reconstruct the top-5 programs for each task because that is all that's present in the logs - because of this, it's important to re-time and re-run DreamCoder on these benchmarks, which we have done and have included outputs in the `out/dc/` subfolders of each benchmark family. Note that we actually cut it down from top-5 to top-K when K<5 in the original DreamCoder run. We always set the number of CPUs to 8 during these re-runs. We can't reconstruct the logLikelihood field of the input so we set it to zero (which is accurate for the majority of domains).

# Format

All data is in `benches/`. This contains 27 folders, one for each historical DreamCoder run. The first underscore-delimited part of the name gives the domain.

Within each run folder, there are benchmark json files, one for each iteration in which DreamCoder accepted at least one new invention. For example `bench006_it8.json` would be the 7th benchmark (where bench000 is the first) which came from the 9th iteration of dreamcoder (where it0 is the first). The benchmark files themselves look like normal DreamCoder input json files (i.e. a grammar and a list of programs grouped by task) with one extra json field `info` giving the number of inventions learned and the resulting grammar.

The subfolder `out/dc/` contains the results of the re-run of DreamCoder on these benchmarks. Subfolder `raw/` contains the stdout output (ie a new grammar and rewritten programs). Subfolder `stderr` contains the stderr output. And subfolder `processed` is the result of analyzing the stdout and stderr to present the learned inventions and various metrics:
- `time_binary_seconds` is the total runtime in seconds of the dreamcoder compression binary
- `time_per_inv_with_rewrite` is the time in milliseconds spent constructing version spaces, running beam search, and rewriting the programs with the new inventions.
- `time_per_inv_no_rewrite` is the same as `time_per_inv_with_rewrite` but without the time spent rewriting
- `mem_peak_kb` is the peak memory usage, obtained by `/usr/bin/time -v`
- `compression_ratio` and `absolute_compression` are particular metrics of compression however you can simply calculate your specific compression metrics yourself on the data in `raw/` instead.

# Re-building the benchmarks

To re-extract the benchmarks from the logs after making any modifications to extraction that you'd like:
- Unzip `dreamcoder_logs.zip` into `dreamcoder_logs/`
- Download and unzip the DreamCoder PLDI artifact into `artifact/`. This should contain a folder `artifact/bin/`.
- Run `./extract_from_logs.sh dreamcoder_logs artifact` which copy `log_extractor.py` into `artifact/bin/` (to give it access to the dreamcoder repo imports) and then run the log parsing procedure on eahc of the log files in the artifact

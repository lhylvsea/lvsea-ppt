# License and Asset Boundaries

## Package rule

`lvsea-ppt` contains only its own routing code, docs, tests and reports. It does not vendor upstream source code, PPTX templates, image assets, fonts, icons, generated outputs or private user material.

## Upstream rules preserved

- AGPL providers such as `dashi-ppt-skill`, `qiaomu-ppt` and `guizang-ppt-skill` remain separate dependencies; consult their licenses before redistribution or network service use.
- `dashi-ppt-skill` README describes a proprietary exporter subpackage. Do not copy it into this repository or extract it for standalone distribution.
- `GordenPPTSkill` documents a personal/research-only restriction for its templates. Do not route enterprise/commercial work to those templates without a separate authorization.
- `gaiduo-ppt` had no LICENSE file in the reviewed checkout; treat its content as “rights to confirm” rather than assume MIT.
- MIT and Apache-2.0 upstream licenses permit method reference, but they do not grant rights to third-party brand marks, downloaded images, fonts, models or user materials.

## Evidence rule

Record URLs, reviewed commit and the precise capability claim in `reports/prior-art-research.md`. “README says it supports X” is not the same as “X ran successfully in this environment”.

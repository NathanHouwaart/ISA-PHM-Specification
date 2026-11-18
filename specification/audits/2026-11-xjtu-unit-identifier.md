# XJTU-SY subset: unit identifier finding

**Follow-up:** The project was re-exported with `G` / `unit:G`; all 568
measurement processes in that later export were verified. The observations
below describe the earlier export and are retained as audit history.

In the locally supplied small-subset export, the first measurement process of
each of the four assays contains the measured-unit value `g` with identifier
`http://qudt.org/vocab/unit/GM`; the assay quantity is QUDT Acceleration.
The Wizard's QUDT 3.5.2 catalogue identifies `unit:GM` as **Gram**, a mass
unit, and `unit:G` as **Gravity**, an acceleration unit. QUDT documents these
as [Gram](https://qudt.org/vocab/unit/GM) and
[Gravity](https://qudt.org/vocab/unit/G), respectively.

Consequently, the current exported unit identifier does not match the stated
quantity. The previous check showing that the Wrapper returned `g` proved
that it read the value, not that the value or identifier was correct. The
selected validator checks also do not currently verify quantity/unit
compatibility. This needs review in the Wizard project and a fresh export.
If gravity is the intended and independently verified unit, the appropriate
Wizard catalogue entry is **Gravity (`G`)**, not **Gram (`g`)**. Do not
rewrite the existing data or change its scientific unit based solely on this
finding; the true measurement unit still needs confirmation from the dataset's
source or researcher.

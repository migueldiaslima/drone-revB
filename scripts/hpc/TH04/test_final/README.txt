Offline test of th04_build.py TH_KEELS (exact keels by point-in-mesh) with TH_CLEAN and TH_ISO (build log item 64),
python3 with numpy, no Abaqus. Mock as test_clean (201,600 tets) with the grid shifted by (0.137, 0.061, 0.093) mm so
no centroid lies on a keel face; fog densities 0.02 to 0.29.
  cd scripts/hpc/TH04/test_final && python3 mkmock.py
  for V in "0.3|KEEL_A_r4.stl,KEEL_B_r4.stl|-54,-23,-11,11,-2,21.5|_F" "0.3|KEEL_A_r4.stl,KEEL_B_r4.stl||_K" \
           "0.3||-54,-23,-11,11,-2,21.5|_C" "0.4x|KEEL_A_r4.stl,KEEL_B_r4.stl|-54,-23,-11,11,-2,21.5|_F40"; do
    IFS='|' read IS KL CL TG <<< "$V"; if [ "$IS" = "0.4x" ]; then unset TH_ISO; else export TH_ISO=$IS; fi
    TH_REV=r4 TH_TAG=$TG TH_KEELS=$KL TH_CLEAN=$CL python3 -I -c "import sys;sys.path.insert(0,'.');sys.argv=['x','c28.odb'];__file__='../th04_build.py';exec(open('../th04_build.py').read())"
  done
  python3 verify.py        -> ALL CHECKS PASS
verify.py selects the keel elements independently (generalized winding number over all triangles, no binning) and
checks the written distribution element by element: solid = rho >= iso, minus TUB design elements in the clean box
outside the keels, plus the keel elements; factors only 1 / 1e-6 (stiffness) and 1 / 1e-9 (mass); fixed always solid.
Result 2026-10-13: keel selection 8,734 elements (1,455.7 mm^3) by both methods, 0 ambiguous; 0 mismatches in all
four cases. Also tested: binned ray test against brute force (3,000 points, 2 directions, 0 mismatches; 60,000 points
in 1.9 s); stop on a wrong TH_KEELS_V and on a missing STL (exit 1 with message); test_clean suite still passes.

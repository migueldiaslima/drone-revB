Offline test of th04_build.py TH_SHAPES / TH_CLEAN (build log item 57), python3 with numpy, no Abaqus.
  cd scripts/hpc/TH04/test_clean && cp ../../../post/keels_r4.py . && python3 mkmock.py
  for V in "A,B|-54,-22,-9,9,0,21.5|_AB" "A|-54,-22,-9,9,0,21.5|_A" "|-54,-22,-9,9,0,21.5|_N" "A,B||_X"; do
    IFS='|' read SH CL TG <<< "$V"
    TH_REV=r4 TH_TAG=$TG TH_SHAPES=$SH TH_CLEAN=$CL python3 -I -c "import sys;sys.path.insert(0,'.');sys.argv=['x','c28.odb'];exec(open('../th04_build.py').read())"
  done
  python3 verify.py        -> ALL CHECKS PASS
Mock: 201,600 tets (1 mm cubes, 6 tets each) over the rear of the tub; fixed deck and spine pad; fog densities 0.02 to 0.3;
a leftover blob (rho 0.85) inside the clean box; wall x > -22 at rho 0.9.

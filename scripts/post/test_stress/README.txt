Offline test of stress_th.py (build log item 66), python3 with numpy, no Abaqus.
  cd scripts/post/test_stress && python3 mkmock.py
  ST_ALLOW_VM=60 ST_ALLOW_T=40 ST_ALLOW_C=70 ST_ALLOW_Z=20 python3 -I -c "import sys;sys.path.insert(0,'.');sys.argv=['x','th.odb','dist_mock.inp'];exec(open('../stress_th.py').read())" > out.txt
  python3 verify.py out.txt     -> checked 48 rows ... ALL CHECKS PASS
Mock: 36,000 tets in three parts (TUB, LID, ARM sets), 60 % solid, 4 integration points per element with an analytic
stress field per step and a 400 MPa outlier in one TUB element (LC3a). verify.py recomputes von Mises (deviator),
principal stresses (np.linalg.eig) and S33 per element, the maximum, 99.9th and 99th percentiles, the utilisation
and the volume above allowable / FS, and compares every printed row. Also tested: stop with a clear message when S is
missing in a step; th04_build.py TH_STRESS=1 adds the S request to the four static steps only (mock deck).

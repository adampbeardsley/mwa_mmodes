pro mmode_test_transfer_calibration

  except=!except
  !except=0
  heap_gc

  ; parse command line args
  compile_opt strictarr
  args = Command_Line_Args(count=nargs)
  vis_file_list = args[0]
  output_directory = args[1]
  version = args[2]
  metafits_path = args[3]
  
  recalculate_all = 1
  max_sources = 200000
  
  calibration_catalog_file_path = filepath('GLEAM_v2_plus_rlb2019.sav',root=rootdir('FHD'),subdir='catalog_data')
  return_cal_visibilities = 1
  pad_uv_image = 1
  diffuse_calibrate = 0
  diffuse_model = 0
  return_sidelobe_catalog = 1
  dft_threshold = 0
  ring_radius = 0
  debug_region_grow = 0
  n_pol = 2
  debug_beam_clip_floor = 1
  model_delay_filter = 1 ; delay filter the model visibilities to get rid of the cyclic beam errors
  
  ; Settings that are special for mmodes
  no_fits=0
  snapshot_healpix_export=0
  cal_bp_transfer=0
  
  transfer_calibration = '/data5/mmodes/fhd_out/fhd_calibrator/calibration/1220459632_158-161_cal.sav'

  fhd_file_list=fhd_path_setup(vis_file_list, version=version, output_directory=output_directory)
  healpix_path=fhd_path_setup(output_dir=output_directory,subdir='Healpix',output_filename='Combined_obs', version=version)


  ; Set global defaults and bundle all the variables into a structure.
  ; Any keywords set on the command line or in the top-level wrapper will supercede these defaults
  eor_wrapper_defaults, extra
  fhd_depreciation_test, _Extra=extra

  print,""
  print,"Keywords set in wrapper:"
  print,structure_to_text(extra)
  print,""

  general_obs,_Extra=extra


end
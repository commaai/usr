#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "hdf5-static" for configuration ""
set_property(TARGET hdf5-static APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5-static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "C"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5-static.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5-static )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5-static "${_IMPORT_PREFIX}/lib/libhdf5-static.a" )

# Import target "hdf5-shared" for configuration ""
set_property(TARGET hdf5-shared APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5-shared PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5-shared.so.1.8.17"
  IMPORTED_SONAME_NOCONFIG "libhdf5-shared.so.10.2.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5-shared )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5-shared "${_IMPORT_PREFIX}/lib/libhdf5-shared.so.1.8.17" )

# Import target "hdf5_tools-static" for configuration ""
set_property(TARGET hdf5_tools-static APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5_tools-static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "C"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5_tools-static.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5_tools-static )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5_tools-static "${_IMPORT_PREFIX}/lib/libhdf5_tools-static.a" )

# Import target "hdf5_tools-shared" for configuration ""
set_property(TARGET hdf5_tools-shared APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5_tools-shared PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5_tools-shared.so.1.8.17"
  IMPORTED_SONAME_NOCONFIG "libhdf5_tools-shared.so.10.2.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5_tools-shared )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5_tools-shared "${_IMPORT_PREFIX}/lib/libhdf5_tools-shared.so.1.8.17" )

# Import target "hdf5_hl-static" for configuration ""
set_property(TARGET hdf5_hl-static APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5_hl-static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "C"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5_hl-static.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5_hl-static )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5_hl-static "${_IMPORT_PREFIX}/lib/libhdf5_hl-static.a" )

# Import target "hdf5_hl-shared" for configuration ""
set_property(TARGET hdf5_hl-shared APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5_hl-shared PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5_hl-shared.so.1.8.17"
  IMPORTED_SONAME_NOCONFIG "libhdf5_hl-shared.so.10.2.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5_hl-shared )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5_hl-shared "${_IMPORT_PREFIX}/lib/libhdf5_hl-shared.so.1.8.17" )

# Import target "hdf5_cpp-static" for configuration ""
set_property(TARGET hdf5_cpp-static APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5_cpp-static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5_cpp-static.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5_cpp-static )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5_cpp-static "${_IMPORT_PREFIX}/lib/libhdf5_cpp-static.a" )

# Import target "hdf5_cpp-shared" for configuration ""
set_property(TARGET hdf5_cpp-shared APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5_cpp-shared PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5_cpp-shared.so.1.8.17"
  IMPORTED_SONAME_NOCONFIG "libhdf5_cpp-shared.so.10.2.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5_cpp-shared )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5_cpp-shared "${_IMPORT_PREFIX}/lib/libhdf5_cpp-shared.so.1.8.17" )

# Import target "hdf5_hl_cpp-static" for configuration ""
set_property(TARGET hdf5_hl_cpp-static APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5_hl_cpp-static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5_hl_cpp-static.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5_hl_cpp-static )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5_hl_cpp-static "${_IMPORT_PREFIX}/lib/libhdf5_hl_cpp-static.a" )

# Import target "hdf5_hl_cpp-shared" for configuration ""
set_property(TARGET hdf5_hl_cpp-shared APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(hdf5_hl_cpp-shared PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libhdf5_hl_cpp-shared.so.1.8.17"
  IMPORTED_SONAME_NOCONFIG "libhdf5_hl_cpp-shared.so.10.2.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf5_hl_cpp-shared )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf5_hl_cpp-shared "${_IMPORT_PREFIX}/lib/libhdf5_hl_cpp-shared.so.1.8.17" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

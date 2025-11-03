from keyGeneration import CADummy

CA = CADummy("NISTP192", 67199102019191)
CA.extract("Auth")
CA.extract("Author01")
CA.extract("LegitimateAuthor")
CA.extract("LegitimateAuthorb9fcec64")
CA.extract("LegitimateAuthord5e0ed0b0574281c")

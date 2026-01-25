-- Seed data for 9th grade English as a Foreign Language vocabulary learning

-- Tags (10 tags for categorizing vocabulary)
INSERT INTO lexloop_tags (uuid, title, description) VALUES
('02424bdb-068e-43b1-8815-cbd9b66a6db6', 'Unit 1 - School Life', 'Vocabulary related to school and education'),
('72ba82b9-d535-4dad-8fa7-1191ff772ee3', 'Unit 2 - Family & Friends', 'Words about relationships and people'),
('f8659072-3400-42ab-8a4b-051d37b2b32b', 'Unit 3 - Daily Routine', 'Everyday activities and habits'),
('11d0b48e-f80a-4d28-89c0-941a22d6fa78', 'Unit 4 - Food & Cooking', 'Culinary vocabulary'),
('5e9cfbc2-c5a6-46fc-b4cc-69269de40442', 'Unit 5 - Travel', 'Transportation and travel-related words'),
('98ff40e8-d8b3-43e5-9573-2247d12532f2', 'Adjectives', 'Descriptive words'),
('e0694e62-b746-4ed0-b24e-be1abb194eda', 'Verbs', 'Action words'),
('9024e5e1-b6cf-4d87-bb4c-a08338e3e79b', 'Nouns', 'People, places, things'),
('a1f0a472-01f7-448f-a28b-d66894ec12f1', 'Tricky Words', 'Commonly confused or difficult words'),
('910596b5-f15a-45be-a941-94c448539023', 'Exam Prep', 'Important vocabulary for upcoming tests');

-- Nodes (30 words for vocabulary learning)
INSERT INTO lexloop_nodes (uuid, title, description) VALUES
-- Synonyms pairs
('bd3f2a56-99d9-4b19-bdba-ca513c0ec652', 'big', 'Large in size'),
('5f61e0a6-c753-446c-b76f-828a9e60f7e8', 'large', 'Of considerable size'),
('5b6d3820-5dba-4e57-9900-698f84d3e283', 'happy', 'Feeling pleasure or joy'),
('f0b5f926-ae24-4732-9ccf-bebbc4b3a250', 'glad', 'Feeling pleased'),
('05980c50-724d-454c-ad92-3c2dd4dc85ff', 'fast', 'Moving quickly'),
('25f34165-8c53-46e0-b378-42bfdf4854c2', 'quick', 'Done with speed'),
-- Antonyms pairs
('1b6de3dd-49a3-4b16-b143-99a1aafba41b', 'hot', 'Having a high temperature'),
('56265a23-07fb-472b-8a00-390689bf15d7', 'cold', 'Having a low temperature'),
('0d3734fc-0938-44ad-a03b-e321f1d5242b', 'old', 'Having lived for many years'),
('4bc4d24d-c4ea-4db0-9da9-ff925ef8eea7', 'young', 'Having lived for a short time'),
('7b17c724-a501-4b79-975e-23550464740d', 'begin', 'To start something'),
('55f04eba-3311-45be-a9e6-d8f14db3fa52', 'end', 'To finish something'),
-- False friends (German-English)
('c5a5fb3e-894d-4c0b-bbea-535a12f7ceff', 'become', 'To start being something'),
('abeb20e2-2266-418b-b2fc-3dc1ce925f23', 'bekommen', 'German: to receive (NOT become!)'),
('e70cef24-54af-4044-a561-62279a2a6149', 'gift', 'Something given as a present'),
('25edfe83-71e1-4bf6-835c-7937364cb9ea', 'Gift', 'German: poison (NOT a present!)'),
('68f4cce5-989f-439a-b090-84a1e44910e6', 'chef', 'Head cook in a kitchen'),
('a1ca3cb0-e60c-4bf6-b54a-2a4e97189618', 'Chef', 'German: boss (NOT a cook!)'),
-- Homophones
('1c9e5bd6-7092-4b90-8203-ef9a60e2fe63', 'their', 'Belonging to them'),
('7a60bad0-f53f-4ce1-8572-4afb8744f7b0', 'there', 'In that place'),
('840d7d42-c26e-4f4f-abda-061181d504cd', 'write', 'To form letters on a surface'),
('b8e3cd0c-bee2-465a-a3cd-eb935212642c', 'right', 'Correct; opposite of left'),
('c24f126f-6a1f-4ff9-bf08-65488a179a3e', 'know', 'To have knowledge of'),
('9e2db5c6-6363-4f42-adc0-430b6ab2c745', 'no', 'Negative response'),
-- Cognates (English-German)
('b03efe64-7f43-46e3-82cb-ba4cd2e6258d', 'house', 'A building for living in'),
('ef0cdc65-64a4-40a2-a58a-35de526bf7c2', 'Haus', 'German: a building for living in'),
('6009753f-0e45-4fd7-9468-eea46c17b740', 'garden', 'An outdoor area with plants'),
('4e0141e2-5bd2-431f-877c-410f82852d4f', 'Garten', 'German: an outdoor area with plants'),
('2ca10fca-e6e9-4d05-a9be-23843c3d2eb9', 'water', 'Clear liquid essential for life'),
('3c364969-9bb7-4f84-8578-0cd3cce783aa', 'Wasser', 'German: clear liquid essential for life');

-- Node-to-Tag associations
INSERT INTO lexloop_node_to_tags (node_uuid, tag_uuid) VALUES
-- Adjectives
('bd3f2a56-99d9-4b19-bdba-ca513c0ec652', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('5f61e0a6-c753-446c-b76f-828a9e60f7e8', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('5b6d3820-5dba-4e57-9900-698f84d3e283', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('f0b5f926-ae24-4732-9ccf-bebbc4b3a250', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('05980c50-724d-454c-ad92-3c2dd4dc85ff', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('25f34165-8c53-46e0-b378-42bfdf4854c2', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('1b6de3dd-49a3-4b16-b143-99a1aafba41b', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('56265a23-07fb-472b-8a00-390689bf15d7', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('0d3734fc-0938-44ad-a03b-e321f1d5242b', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('4bc4d24d-c4ea-4db0-9da9-ff925ef8eea7', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
-- Verbs
('7b17c724-a501-4b79-975e-23550464740d', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('55f04eba-3311-45be-a9e6-d8f14db3fa52', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('c5a5fb3e-894d-4c0b-bbea-535a12f7ceff', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('840d7d42-c26e-4f4f-abda-061181d504cd', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('c24f126f-6a1f-4ff9-bf08-65488a179a3e', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
-- Nouns
('e70cef24-54af-4044-a561-62279a2a6149', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('68f4cce5-989f-439a-b090-84a1e44910e6', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('b03efe64-7f43-46e3-82cb-ba4cd2e6258d', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('6009753f-0e45-4fd7-9468-eea46c17b740', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('2ca10fca-e6e9-4d05-a9be-23843c3d2eb9', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
-- Tricky Words (false friends and homophones)
('c5a5fb3e-894d-4c0b-bbea-535a12f7ceff', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('abeb20e2-2266-418b-b2fc-3dc1ce925f23', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('e70cef24-54af-4044-a561-62279a2a6149', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('25edfe83-71e1-4bf6-835c-7937364cb9ea', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('68f4cce5-989f-439a-b090-84a1e44910e6', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('a1ca3cb0-e60c-4bf6-b54a-2a4e97189618', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('1c9e5bd6-7092-4b90-8203-ef9a60e2fe63', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('7a60bad0-f53f-4ce1-8572-4afb8744f7b0', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('840d7d42-c26e-4f4f-abda-061181d504cd', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('b8e3cd0c-bee2-465a-a3cd-eb935212642c', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('c24f126f-6a1f-4ff9-bf08-65488a179a3e', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('9e2db5c6-6363-4f42-adc0-430b6ab2c745', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
-- Exam Prep (common vocabulary)
('bd3f2a56-99d9-4b19-bdba-ca513c0ec652', '910596b5-f15a-45be-a941-94c448539023'),
('5b6d3820-5dba-4e57-9900-698f84d3e283', '910596b5-f15a-45be-a941-94c448539023'),
('1b6de3dd-49a3-4b16-b143-99a1aafba41b', '910596b5-f15a-45be-a941-94c448539023'),
('7b17c724-a501-4b79-975e-23550464740d', '910596b5-f15a-45be-a941-94c448539023'),
('b03efe64-7f43-46e3-82cb-ba4cd2e6258d', '910596b5-f15a-45be-a941-94c448539023');

-- Links (various relationship types)
INSERT INTO lexloop_links (uuid, type, annotation, node1_uuid, node2_uuid) VALUES
-- Synonyms
('af6e400e-6d65-4116-ba34-8276cf91ea31', 'SYNONYM', 'Both describe something of considerable size', 'bd3f2a56-99d9-4b19-bdba-ca513c0ec652', '5f61e0a6-c753-446c-b76f-828a9e60f7e8'),
('9aaa5cc8-387a-492d-8018-6b5dea9d2455', 'SYNONYM', 'Both express positive emotions', '5b6d3820-5dba-4e57-9900-698f84d3e283', 'f0b5f926-ae24-4732-9ccf-bebbc4b3a250'),
('ff1cc70a-6445-4ed7-816e-f365cd566a2f', 'SYNONYM', 'Both describe high speed', '05980c50-724d-454c-ad92-3c2dd4dc85ff', '25f34165-8c53-46e0-b378-42bfdf4854c2'),
-- Antonyms
('744ea99c-11f7-46e4-a725-a06039d7d1a8', 'ANTONYM', 'Opposite temperature extremes', '1b6de3dd-49a3-4b16-b143-99a1aafba41b', '56265a23-07fb-472b-8a00-390689bf15d7'),
('b017ecfb-e93b-4d09-865d-7deb5507e6ad', 'ANTONYM', 'Opposite ends of the age spectrum', '0d3734fc-0938-44ad-a03b-e321f1d5242b', '4bc4d24d-c4ea-4db0-9da9-ff925ef8eea7'),
('5c12634f-007e-46bc-b3e7-4a73ac187cc0', 'ANTONYM', 'Opposite points in time/process', '7b17c724-a501-4b79-975e-23550464740d', '55f04eba-3311-45be-a9e6-d8f14db3fa52'),
-- False Friends
('2870c418-6d53-4178-8f75-7d3e370150a4', 'FALSE_FRIEND', 'bekommen means "to get/receive" not "to become"', 'c5a5fb3e-894d-4c0b-bbea-535a12f7ceff', 'abeb20e2-2266-418b-b2fc-3dc1ce925f23'),
('f79aaf4f-4975-484b-a3e8-080e269bb54f', 'FALSE_FRIEND', 'German Gift means poison, not a present!', 'e70cef24-54af-4044-a561-62279a2a6149', '25edfe83-71e1-4bf6-835c-7937364cb9ea'),
('b24acc05-886a-4152-b2be-45985d622d99', 'FALSE_FRIEND', 'German Chef means boss, not a cook!', '68f4cce5-989f-439a-b090-84a1e44910e6', 'a1ca3cb0-e60c-4bf6-b54a-2a4e97189618'),
-- Homophones
('2a6ce10d-b94f-49a7-9364-19d9870be369', 'HOMOPHONE', 'Same pronunciation /ðeər/', '1c9e5bd6-7092-4b90-8203-ef9a60e2fe63', '7a60bad0-f53f-4ce1-8572-4afb8744f7b0'),
('631ccfbb-2952-4de9-97b8-06f8c199fc8f', 'HOMOPHONE', 'Same pronunciation /raɪt/', '840d7d42-c26e-4f4f-abda-061181d504cd', 'b8e3cd0c-bee2-465a-a3cd-eb935212642c'),
('f16d1873-679d-498a-82e4-3bba123a862a', 'HOMOPHONE', 'Same pronunciation /noʊ/', 'c24f126f-6a1f-4ff9-bf08-65488a179a3e', '9e2db5c6-6363-4f42-adc0-430b6ab2c745'),
-- Cognates
('2e34566d-65e6-4e87-90d5-101d716bd341', 'COGNATE', 'Same Germanic root, similar spelling and meaning', 'b03efe64-7f43-46e3-82cb-ba4cd2e6258d', 'ef0cdc65-64a4-40a2-a58a-35de526bf7c2'),
('76c155d3-d621-42e7-a1ce-e53bd41ebca5', 'COGNATE', 'Same Germanic root, similar spelling and meaning', '6009753f-0e45-4fd7-9468-eea46c17b740', '4e0141e2-5bd2-431f-877c-410f82852d4f'),
('440fcbb4-b2ad-4d33-b5f5-81d983e53fec', 'COGNATE', 'Same Germanic root, similar spelling and meaning', '2ca10fca-e6e9-4d05-a9be-23843c3d2eb9', '3c364969-9bb7-4f84-8578-0cd3cce783aa');

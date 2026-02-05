-- Seed data for 9th grade English as a Foreign Language vocabulary learning

INSERT INTO lexloop_courses (uuid, name) VALUES
('59cc5186-a10d-476e-b750-c8f5b821b953', 'Base Course'),
('0419df0c-080f-4a93-bb4e-82fc6121b073', 'Empty Course');

-- Tags
INSERT INTO lexloop_tags (uuid, title, description, course_uuid) VALUES
('1f86242e-242f-4019-9157-a0d3d6695f68', 'Unit: Australia', '', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('202f12bd-aa32-4d30-8ca9-f8a4a13c9668', 'Feelings', '', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('556412af-be74-45d1-91ad-b9194dff4cfc', 'Unit: New Zealand ', '', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('57e24f72-43fa-434d-8aac-f96a2ba0b5ac', 'Unit: The Northeast of England', '', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('683ed950-6015-4a00-865a-d8b0330423a0', 'Prepositions', '', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('9024e5e1-b6cf-4d87-bb4c-a08338e3e79b', 'Nouns', 'People, places, things', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('910596b5-f15a-45be-a941-94c448539023', 'Exam Prep', 'Important vocabulary for upcoming tests', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('98ff40e8-d8b3-43e5-9573-2247d12532f2', 'Adjectives', 'Descriptive words', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('9a299d07-5d04-406d-b252-e69302fa6b79', 'Unit: The Southwest of the USA', '', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('a1f0a472-01f7-448f-a28b-d66894ec12f1', 'Tricky Words', 'Commonly confused or difficult words', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('e0694e62-b746-4ed0-b24e-be1abb194eda', 'Verbs', 'Action words', '59cc5186-a10d-476e-b750-c8f5b821b953');

-- Nodes (30 words for vocabulary learning)
INSERT INTO lexloop_nodes (uuid, title, description, course_uuid) VALUES
('05980c50-724d-454c-ad92-3c2dd4dc85ff', 'fast', 'Moving quickly', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('0d3734fc-0938-44ad-a03b-e321f1d5242b', 'old', 'Having lived for many years', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('1b6de3dd-49a3-4b16-b143-99a1aafba41b', 'hot', 'Having a high temperature', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('1c9e5bd6-7092-4b90-8203-ef9a60e2fe63', 'their', 'Belonging to them', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('25f34165-8c53-46e0-b378-42bfdf4854c2', 'quick', 'Done with speed', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('2ca10fca-e6e9-4d05-a9be-23843c3d2eb9', 'water', 'Clear liquid essential for life', '59cc5186-a10d-476e-b750-c8f5b821b953'), ('2dd453db-a93d-4645-9070-81a8bd51c7fb', 'picture', 'Übersetzung: Bild ', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('47890618-6af3-4e04-a012-d546096024ab', 'outdoor', 'existing, happening or done outside, rather than inside a building.

Chunks: Outdoor time, spend time outdoors ', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('4bc4d24d-c4ea-4db0-9da9-ff925ef8eea7', 'young', 'Having lived for a short time', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('510a20c6-e818-44a5-a57b-a9e847f58950', 'to photograph', 'to take a picture

Übersetzung: ein Foto machen

Pronunciation: to ''photograph

Example: I like to photograph birds. She photographs the sunset. ', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('55f04eba-3311-45be-a9e6-d8f14db3fa52', 'end', 'To finish something', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('56265a23-07fb-472b-8a00-390689bf15d7', 'cold', 'Having a low temperature', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('5b6d3820-5dba-4e57-9900-698f84d3e283', 'happy', 'Feeling pleasure or joy', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('5f61e0a6-c753-446c-b76f-828a9e60f7e8', 'large', 'Of considerable size', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('6009753f-0e45-4fd7-9468-eea46c17b740', 'garden', 'An outdoor area with plants', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('68f4cce5-989f-439a-b090-84a1e44910e6', 'chef', 'Head cook in a kitchen', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('728aa600-2d35-4e3e-baff-d7136d3d1cb6', 'camera', 'a device for taking photographs or making films

Übersetzung: Kamera', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('7a60bad0-f53f-4ce1-8572-4afb8744f7b0', 'there', 'In that place', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('7b17c724-a501-4b79-975e-23550464740d', 'begin', 'To start something', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('840d7d42-c26e-4f4f-abda-061181d504cd', 'write', 'To form letters on a surface', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('9e2db5c6-6363-4f42-adc0-430b6ab2c745', 'no', 'Negative response', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('a5f38af4-6e29-4482-af56-30224b3b6bc1', 'memory', 'the power to retain and recall information and past experiences

Übersetzung: Erinnerung', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('b03efe64-7f43-46e3-82cb-ba4cd2e6258d', 'house', 'A building for living in', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('b1c5e908-dab4-4c69-920f-796a785d6b44', 'photo', 'a picture

Übersetzung: Bild
', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('b8e3cd0c-bee2-465a-a3cd-eb935212642c', 'right', 'Correct; opposite of left', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('bd3f2a56-99d9-4b19-bdba-ca513c0ec652', 'big', 'Large in size', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('c24f126f-6a1f-4ff9-bf08-65488a179a3e', 'know', 'To have knowledge of', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('c5a5fb3e-894d-4c0b-bbea-535a12f7ceff', 'become', 'To start being something', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('e4eec2f9-0a0e-45b5-99c1-c3b7201980ab', 'photographer', 'a person who takes photos, especially as a job

Übersetzung: Fotograf
Pronunciation: Pho‘tographer

Example:
My friend wants to be a photographer when he is older.
The photographer took a nice picture.
', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('e70cef24-54af-4044-a561-62279a2a6149', 'gift', 'Something given as a present', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('f0b5f926-ae24-4732-9ccf-bebbc4b3a250', 'glad', 'Feeling pleased','59cc5186-a10d-476e-b750-c8f5b821b953');

-- Node-to-Tag associations
INSERT INTO lexloop_node_to_tags (node_uuid, tag_uuid) VALUES
('05980c50-724d-454c-ad92-3c2dd4dc85ff', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('0d3734fc-0938-44ad-a03b-e321f1d5242b', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('1b6de3dd-49a3-4b16-b143-99a1aafba41b', '910596b5-f15a-45be-a941-94c448539023'),
('1b6de3dd-49a3-4b16-b143-99a1aafba41b', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('1c9e5bd6-7092-4b90-8203-ef9a60e2fe63', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('25f34165-8c53-46e0-b378-42bfdf4854c2', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('2ca10fca-e6e9-4d05-a9be-23843c3d2eb9', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('2dd453db-a93d-4645-9070-81a8bd51c7fb', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('47890618-6af3-4e04-a012-d546096024ab', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('4bc4d24d-c4ea-4db0-9da9-ff925ef8eea7', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('510a20c6-e818-44a5-a57b-a9e847f58950', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('55f04eba-3311-45be-a9e6-d8f14db3fa52', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('56265a23-07fb-472b-8a00-390689bf15d7', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('5b6d3820-5dba-4e57-9900-698f84d3e283', '910596b5-f15a-45be-a941-94c448539023'),
('5b6d3820-5dba-4e57-9900-698f84d3e283', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('5f61e0a6-c753-446c-b76f-828a9e60f7e8', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('6009753f-0e45-4fd7-9468-eea46c17b740', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('68f4cce5-989f-439a-b090-84a1e44910e6', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('68f4cce5-989f-439a-b090-84a1e44910e6', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('728aa600-2d35-4e3e-baff-d7136d3d1cb6', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('7a60bad0-f53f-4ce1-8572-4afb8744f7b0', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('7b17c724-a501-4b79-975e-23550464740d', '910596b5-f15a-45be-a941-94c448539023'),
('7b17c724-a501-4b79-975e-23550464740d', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('840d7d42-c26e-4f4f-abda-061181d504cd', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('840d7d42-c26e-4f4f-abda-061181d504cd', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('9e2db5c6-6363-4f42-adc0-430b6ab2c745', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('a5f38af4-6e29-4482-af56-30224b3b6bc1', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('b03efe64-7f43-46e3-82cb-ba4cd2e6258d', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('b03efe64-7f43-46e3-82cb-ba4cd2e6258d', '910596b5-f15a-45be-a941-94c448539023'),
('b8e3cd0c-bee2-465a-a3cd-eb935212642c', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('bd3f2a56-99d9-4b19-bdba-ca513c0ec652', '910596b5-f15a-45be-a941-94c448539023'),
('bd3f2a56-99d9-4b19-bdba-ca513c0ec652', '98ff40e8-d8b3-43e5-9573-2247d12532f2'),
('c24f126f-6a1f-4ff9-bf08-65488a179a3e', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('c24f126f-6a1f-4ff9-bf08-65488a179a3e', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('c5a5fb3e-894d-4c0b-bbea-535a12f7ceff', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('c5a5fb3e-894d-4c0b-bbea-535a12f7ceff', 'e0694e62-b746-4ed0-b24e-be1abb194eda'),
('e4eec2f9-0a0e-45b5-99c1-c3b7201980ab', '57e24f72-43fa-434d-8aac-f96a2ba0b5ac'),
('e4eec2f9-0a0e-45b5-99c1-c3b7201980ab', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('e70cef24-54af-4044-a561-62279a2a6149', '9024e5e1-b6cf-4d87-bb4c-a08338e3e79b'),
('e70cef24-54af-4044-a561-62279a2a6149', 'a1f0a472-01f7-448f-a28b-d66894ec12f1'),
('f0b5f926-ae24-4732-9ccf-bebbc4b3a250', '202f12bd-aa32-4d30-8ca9-f8a4a13c9668'),
('f0b5f926-ae24-4732-9ccf-bebbc4b3a250', '98ff40e8-d8b3-43e5-9573-2247d12532f2');

-- Links (various relationship types)
INSERT INTO lexloop_links (uuid, type, annotation, node1_uuid, node2_uuid, course_uuid) VALUES
('08501ef6-26a8-47bd-a201-ffa6b9f91be5', 'WORD_FAMILY', '', 'b1c5e908-dab4-4c69-920f-796a785d6b44', 'e4eec2f9-0a0e-45b5-99c1-c3b7201980ab', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('2a6ce10d-b94f-49a7-9364-19d9870be369', 'HOMOPHONE', 'Same pronunciation /ðeər/', '1c9e5bd6-7092-4b90-8203-ef9a60e2fe63', '7a60bad0-f53f-4ce1-8572-4afb8744f7b0', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('3456752f-d463-43ec-aa03-32837bca756c', 'WORD_FAMILY', '', '510a20c6-e818-44a5-a57b-a9e847f58950', 'e4eec2f9-0a0e-45b5-99c1-c3b7201980ab', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('5c12634f-007e-46bc-b3e7-4a73ac187cc0', 'ANTONYM', 'Opposite points in time/process', '7b17c724-a501-4b79-975e-23550464740d', '55f04eba-3311-45be-a9e6-d8f14db3fa52', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('631ccfbb-2952-4de9-97b8-06f8c199fc8f', 'HOMOPHONE', 'Same pronunciation /raɪt/', '840d7d42-c26e-4f4f-abda-061181d504cd', 'b8e3cd0c-bee2-465a-a3cd-eb935212642c', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('744ea99c-11f7-46e4-a725-a06039d7d1a8', 'ANTONYM', 'Opposite temperature extremes', '1b6de3dd-49a3-4b16-b143-99a1aafba41b', '56265a23-07fb-472b-8a00-390689bf15d7', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('852dc7ca-ddfb-4b49-84f8-0d0ca203ac70', 'SYNONYM', '', '2dd453db-a93d-4645-9070-81a8bd51c7fb', 'b1c5e908-dab4-4c69-920f-796a785d6b44', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('9aaa5cc8-387a-492d-8018-6b5dea9d2455', 'SYNONYM', 'Both express positive emotions', '5b6d3820-5dba-4e57-9900-698f84d3e283', 'f0b5f926-ae24-4732-9ccf-bebbc4b3a250', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('af6e400e-6d65-4116-ba34-8276cf91ea31', 'SYNONYM', 'Both describe something of considerable size', 'bd3f2a56-99d9-4b19-bdba-ca513c0ec652', '5f61e0a6-c753-446c-b76f-828a9e60f7e8', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('b017ecfb-e93b-4d09-865d-7deb5507e6ad', 'ANTONYM', 'Opposite ends of the age spectrum', '0d3734fc-0938-44ad-a03b-e321f1d5242b', '4bc4d24d-c4ea-4db0-9da9-ff925ef8eea7', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('d4f814e8-497e-4c8a-8658-e53dea9c1109', 'WORD_FAMILY', '', 'b1c5e908-dab4-4c69-920f-796a785d6b44', '510a20c6-e818-44a5-a57b-a9e847f58950', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('f16d1873-679d-498a-82e4-3bba123a862a', 'HOMOPHONE', 'Same pronunciation /noʊ/', 'c24f126f-6a1f-4ff9-bf08-65488a179a3e', '9e2db5c6-6363-4f42-adc0-430b6ab2c745', '59cc5186-a10d-476e-b750-c8f5b821b953'),
('ff1cc70a-6445-4ed7-816e-f365cd566a2f', 'SYNONYM', 'Both describe high speed', '05980c50-724d-454c-ad92-3c2dd4dc85ff', '25f34165-8c53-46e0-b378-42bfdf4854c2', '59cc5186-a10d-476e-b750-c8f5b821b953');

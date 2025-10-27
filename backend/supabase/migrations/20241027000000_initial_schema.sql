-- Create nodes table
CREATE TABLE IF NOT EXISTS nodes (
    uuid UUID PRIMARY KEY,
    term TEXT NOT NULL,
    definition TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create links table
CREATE TABLE IF NOT EXISTS links (
    uuid UUID PRIMARY KEY,
    type TEXT NOT NULL,
    node1_uuid UUID NOT NULL REFERENCES nodes(uuid),
    node2_uuid UUID NOT NULL REFERENCES nodes(uuid),
    annotation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for link lookups
CREATE INDEX IF NOT EXISTS idx_links_node1 ON links(node1_uuid);
CREATE INDEX IF NOT EXISTS idx_links_node2 ON links(node2_uuid);


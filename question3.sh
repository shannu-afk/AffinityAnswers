if [ $# -ne 1 ]; then
    echo "Usage: $0 <url>" >&2
    exit 1
fi

URL="$1"

curl -s "$URL" | \
tail -n +2 | \
awk -F',' '{
    # Reconstruct company name (field 2) in case it contains commas
    name = $2
    gsub(/^"/, "", name)
    gsub(/"$/, "", name)

    # Location is field 5
    location = $5
    gsub(/^"/, "", location)
    gsub(/"$/, "", location)

    # Founding year is last field
    year = $NF
    gsub(/"/, "", year)

    # Handle cases like "1998 (1888)" → extract earliest year in parentheses if present
    if (match(year, /\([0-9]+\)/)) {
        year = substr(year, RSTART+1, RLENGTH-2)
    } else if (match(year, /^[0-9]+/)) {
        year = substr(year, RSTART, RLENGTH)
    } else {
        year = "0000"
    }

    # Print tab-separated
    print year "\t" name "\t" location
}' | \
sort -n | \
awk -F'\t' '{
    # Skip invalid years
    if ($1 != "0000") print $2 "\t" $3 "\t" $1
}'
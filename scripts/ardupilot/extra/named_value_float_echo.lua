local NAMED_VALUE_FLOAT = {}
NAMED_VALUE_FLOAT.id = 251
NAMED_VALUE_FLOAT.fields = {
    { "time_boot_ms", "<I4" },
    { "value", "<f" },
    { "name", "<c10" },
}

local function decode_named_value_float(message)
    local result = {}
    local offset = 2  -- Start from the second byte

    for _, field in ipairs(NAMED_VALUE_FLOAT.fields) do
        local value
        local success, err = pcall(function()
            value, offset = string.unpack(field[2], message, offset)
        end)
        if not success then
            return nil
        end
        result[field[1]] = value
    end
    return result
end

local function bytes_to_string(str)
    return str:match("^%z*(.-)%z*$")  -- Remove leading and trailing null bytes
end

local function hex_dump(str)
    return (str:gsub('.', function (c) return string.format('%02X ', string.byte(c)) end))
end

mavlink.init(1, 10)
mavlink.register_rx_msgid(NAMED_VALUE_FLOAT.id)

function update()
    local msg, _, timestamp_ms = mavlink.receive_chan()
    if msg then
        
        local header = msg:sub(1, 10)  -- MAVLink v2 header is 10 bytes
        local payload = msg:sub(12)    -- Payload starts at 11th byte for MAVLink v2

        local decoded_msg = decode_named_value_float(payload)
        if decoded_msg then
            local name = bytes_to_string(decoded_msg.name)
            local value = decoded_msg.value
            --gcs:send_text(6, string.format("Received NAMED_VALUE_FLOAT: %s = %f", name, value))
            gcs:send_named_float(name, value)
        end
    end
    return update, 100
end

return update()
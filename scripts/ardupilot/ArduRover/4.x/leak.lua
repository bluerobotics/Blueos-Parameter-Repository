-- Leak detection/failsafe functionality for the Navigator
-- Intended for use with ArduRover (e.g. on a BlueBoat)

---- USER CONFIG ----
local warning_interval_ms = uint32_t(15000)  -- warn every 15s

-- specify 1-2 failsafe modes for desired behaviour
RoverMode = {
    Hold = 4,
    Loiter = 5,
    RTL = 11,
    SmartRTL = 12,
}
local failsafe_mode = {RoverMode.Loiter, RoverMode.Hold}  -- try to loiter, otherwise hold
---------------------

-- perform setup
local navigator_leak_pin = 27
gpio:pinMode(navigator_leak_pin,0)  -- configure as a digital input
local warning_last_sent = uint32_t()

-- define the loop
function update()
    if gpio:read(navigator_leak_pin) then
        -- warn the operator, if they haven't been warned recently
        if millis() - warning_last_sent > warning_interval_ms then
            gcs:send_text(2, "Leak detected!")  -- critical level announcement
            warning_last_sent = millis()
        end
        -- change mode, with an optional fallback
        local current_mode = vehicle:get_mode()
        if (
          current_mode ~= failsafe_mode[1] and current_mode ~= failsafe_mode[2]  -- not already changed
          and not vehicle:set_mode(failsafe_mode[1])  -- AND first change doesn't work
          and failsafe_mode[2]  -- AND backup mode provided
        ) then
            vehicle:set_mode(failsafe_mode[2])
        end
    end

    return update, 1000  -- check again after 1s
end

-- start the loop (immediately)
return update()

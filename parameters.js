var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
define("hardware/power_sense", ["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.POWER_SENSE_MODULE = void 0;
    exports.POWER_SENSE_MODULE = {
        BATT_CAPACITY: 0.0,
        BATT_AMP_OFFSET: 0.330,
        BATT_AMP_PERVLT: 37.8788,
        BATT_VOLT_MULT: 11.000,
        BATT_MONITOR: 4,
    };
});
define("4.1/base", ["require", "exports", "hardware/power_sense"], function (require, exports, power_sense_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.BASE_BLUEROV = void 0;
    exports.BASE_BLUEROV = __assign(__assign({}, power_sense_1.POWER_SENSE_MODULE), { AHRS_ORIENTATION: 16, BRD_RTC_TYPES: 3, MNT_RC_IN_TILT: 8, MNT_TYPE: 1, SERIAL0_PROTOCOL: 2 });
});
define("4.1/heavy", ["require", "exports", "4.1/base"], function (require, exports, base_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    var SERVOS_HEAVY = {
        SERVO7_FUNCTION: 39,
        SERVO8_FUNCTION: 40,
        SERVO8_REVERSED: 0,
        SERVO9_FUNCTION: 59,
        SERVO10_FUNCTION: 7,
        SERVO10_REVERSED: 1,
    };
    var BLUEROV2_HEAVY = __assign(__assign({}, base_1.BASE_BLUEROV), { ATC_ANG_PIT_P: 6.0, ATC_ANG_RLL_P: 6.0, ATC_ANG_YAW_P: 6.0, FRAME_CONFIG: 2 });
});
define("4.1/standard", ["require", "exports", "4.1/base"], function (require, exports, base_2) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    var BLUEROV_STANDARD = __assign(__assign({}, base_2.BASE_BLUEROV), { ATC_ANG_RLL_P: 0.0, FRAME_CONFIG: 1 });
});
define("hardware/boards", ["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.SERVOS_STANDARD_PIXHAWK = exports.NAVIGATOR = exports.PIXHAWK1 = void 0;
    exports.PIXHAWK1 = {
        LEAK1_PIN: 55,
    };
    exports.NAVIGATOR = {
        LEAK1_PIN: 27,
    };
    exports.SERVOS_STANDARD_PIXHAWK = {
        SERVO7_FUNCTION: 59,
        SERVO8_FUNCTION: 7,
        SERVO8_REVERSED: 1,
    };
});
//# sourceMappingURL=out.js.map
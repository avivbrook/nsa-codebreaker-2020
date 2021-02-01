#include <stdbool.h>

static bool alt = false;

char *GPSNMEA(void) {
    alt = !alt;
    return alt ? "$GNGGA,233900.669,0513.78,N,02459.58,W,1,8,,100.0,M,,,,*61" : "$GNRMC,233900.669,A,00513.78,N,02459.58,W,0.0,,091020,,,A*95";
}
#include <stdio.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "led_controller.h"
#include "esp_log.h"

static const char *TAG = "wifi station";

void app_main(void)
{
    //Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    ws2812_control_init();
    
    struct tm timeinfo;

    while(1)
    {
        timeinfo = get_time();
        led_clock(timeinfo);
        vTaskDelay(200 / portTICK_PERIOD_MS);
    }
    

    //time_test();
    //led_test();

}

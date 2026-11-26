#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define KEY_COUNT 11
#define USERNAME "nLYTCmdXobFRhs"

uint16_t transform_value(uint16_t value, uint16_t index, size_t username_length)
{

    uint16_t result = ~(value - index);

    result = result ^ index;

    result = result ^ username_length;

    return result;
}

void generate_key(uint16_t values[], uint16_t keys[], size_t username_length)
{
    for (int i = 0; i < KEY_COUNT; i++)
    {
        keys[i] = transform_value(values[i], i, username_length);
    };
}

int main()
{
    uint16_t bytes[KEY_COUNT] = {
        0xffb1, 0xff98, 0xffa0, 0xff9c, 0xffb8, 0xff99, 0xffa2, 0xffe0, 0xffe2, 0xffb2, 0xffff};

    uint16_t keys[KEY_COUNT];

    generate_key(bytes, keys , strlen(USERNAME));

    for (int i = 0; i < KEY_COUNT; i++)
    {
        printf("[%i/11] %i\n", i + 1, keys[i]);
    }
}
#include <stdio.h>
#include <unistd.h>
#include <time.h>

int main() {
  time_t timer;
  char buffer[26];
  struct tm* tm_info;

  puts("start");
  while (42) {
    time(&timer);
    tm_info = localtime(&timer);

    strftime(buffer, 26, "%Y-%m-%d %H:%M:%S", tm_info);
    puts(buffer);
    sleep(5);
  }
}

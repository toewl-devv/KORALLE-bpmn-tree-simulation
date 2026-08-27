#include <locale.h>
#include <iostream>
#include <ncurses.h>

using namespace std;

int main() {
    setlocale(LC_ALL, "");
    initscr();
    noecho();
    curs_set(0);
    int mode = 0;
    while (true) {
        mvprintw(0, 0, "Tree Builder");
        refresh();

        int key = getch();
        if (mode == 0) {
            if (key == ':') {
                mode = 1;
            }
            if (key == 'q') {
                break;
            }
        }
        if (mode == 1) {
            //typing mechanics
        }
        
    }
    endwin();

    return 0;
}

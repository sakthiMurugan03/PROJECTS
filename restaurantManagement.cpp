#include <iostream>
#include <string>
#include <iomanip>
#include <vector>

using namespace std;

// Class for handling table reservations
class Table_reservation {
public:
    string type, dining;

    void reserve(string type) {
        this->type = type;
        cout<<"\n(1. Family dining) \n(2. Couple dining) \n(3. Single dining)";
        cout << "\nEnter your preferred type of dining:  ";
        std::getline(std::cin >> std::ws, dining);
    }

    void display_reservation() const {
        cout << "\n\nReservation Details:\n";
        cout << setw(25) << left << "Type (AC/NON-AC):" << setw(15) << left << type << endl;
        cout << setw(25) << left << "Type of dining:" << setw(15) << left << dining << endl;
    }
};

// Class representing the restaurant
class Restaurant {
public:
    string r_type;

    void setr(const string& r_type) {
        this->r_type = r_type;
    }

    void getr() const {
        cout << setw(25) << left << "Restaurant Type:" << setw(15) << left << r_type << endl;
    }
};

// Class representing a client
class Client : public Table_reservation {
public:
    string name;
    int id;
    int client_no;
    string card_num;

    Client() {}
    Client(const string& name, int id, int client_no, const string& card_num)
        : name(name), id(id), client_no(client_no), card_num(card_num) {}

    void getclient() const {
        cout << "\n\nClient Details:\n";
        cout << setw(25) << left << "Client Name:" << setw(15) << left << name << endl;
        cout << setw(25) << left << "Booking ID:" << setw(15) << left << id << endl;
        cout << setw(25) << left << "Number of Guests:" << setw(15) << left << client_no << endl;
        cout << setw(25) << left << "Card Number:" << setw(15) << left << card_num << endl;
    }
};

int main() {
    vector<string> food;
    vector<int> price;
    // Initializing food items and prices
    food.push_back("Cheese Burgers"); price.push_back(120);
    food.push_back("Plain Dosa"); price.push_back(50);
    food.push_back("Butter Naan"); price.push_back(90);
    food.push_back("Romali Roti"); price.push_back(40);
    food.push_back("Lentil Soup"); price.push_back(45);
    food.push_back("Fruit Salad"); price.push_back(35);
    food.push_back("Sandwich"); price.push_back(96);
    food.push_back("French Fries"); price.push_back(40);
    food.push_back("Veg Nuggets"); price.push_back(120);
    food.push_back("Milkshake"); price.push_back(50);
    food.push_back("Falooda"); price.push_back(70);
    food.push_back("Ice-cream"); price.push_back(90);
    food.push_back("Cold-Coffee"); price.push_back(60);
    food.push_back("Rasgulla"); price.push_back(90);

    int s = 0, amt = 0;
    vector<int> orderp(20, 0);
    vector<string> order(20);
    string continue1, reply;

    cout << setw(80) << "** A PLACE WHERE MEMORIES ARE MADE !!! **\n";
    cout << setw(75) << "** Welcome to ENIGMA EMPORIUM ***\n\n";
    Restaurant r;
    r.setr("5-star");
    r.getr();

    Client c("Pooja", 1000, 4, "NOO7612");
    c.getclient();

    Table_reservation t;
    t.reserve("AC");
    t.display_reservation();


    cout << "\n \t\t MENU CARD\n";

    do {
        cout << "\n\t1. Main Course \n\t2. Appetizers \n\t3. Desserts \n\n";
        cout << "\nEnter your meal preference: ";
        int ch;
        cin >> ch;

        int start = 0, end = 0;
        if (ch == 1) { start = 0; end = 3; }
        else if (ch == 2) { start = 4; end = 8; }
        else if (ch == 3) { start = 9; end = 13; }
        else {
            cout << "\nSorry, invalid entry...\n" << endl;
            continue;
        }

        do {
            for (int i = start; i <= end; ++i) {
                cout << "\n" << setw(30) << left << food[i] << "\t\t" << price[i];
            }
            cout << endl;

            cout << "\nWhat would you like to eat? ";
            cin.ignore();
            getline(cin, order[s]);

            bool found = false;
            for (int i = start; i <= end; ++i) {
                if (order[s] == food[i]) {
                    amt += price[i];
                    orderp[s] = price[i];
                    cout << "\n" << food[i] << " successfully placed..!";
                    s++;
                    found = true;
                    break;
                }
            }
            if (!found) {
                cout << "\nInvalid selection, please try again.";
            }

            cout << "\n\nDo you want to order something else? (yes/no): ";
            cin >> continue1;
        } while (continue1 == "yes");

        cout << "\nWould you like to try any other dishes? (yes/no): ";
        cin >> reply;
    } while (reply == "yes");

    cout << "\n\n" << setw(80) << "Toll free no : 8072497758" << endl;
    cout << setw(60) << "Address : No.6," << endl;
    cout << setw(80) << "Dubai Kurukku Sandhu," << endl;
    cout << setw(80) << "Vivekanandhar Theru," << endl;
    cout << setw(75) << "Dubai Main Road," << endl;
    cout << setw(60) << "Dubai." << endl;

    cout << "\nOrder Summary:\n";
    for (int a = 0; a < s; ++a) {
        if (orderp[a] != 0) {
            cout << "\n\t" << setw(30) << left << order[a] << setw(15) << left << orderp[a];
        }
    }
    cout << "\n\n\t\t"<< "Total Price: " << amt << "\n" << endl;
    cout<<"\tTHANK YOU !! PLEASE VISIT AGAIN !!"<<endl;

    
    return 0;
}

 

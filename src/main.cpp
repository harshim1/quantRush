#include <iostream>
#include <vector>
#include <queue>
#include <map>
#include <chrono>
#include <thread>
#include <random>
#include <cmath>

// Struct representing an order
struct Order {
    int id;
    double price;
    int quantity;
    bool is_buy;
    std::chrono::high_resolution_clock::time_point timestamp;
};

// OrderBook class to simulate limit order book behavior
class OrderBook {
private:
    std::map<double, std::queue<Order>, std::greater<double>> buy_orders;
    std::map<double, std::queue<Order>> sell_orders;
    int order_id_counter = 0;

public:
    void place_order(double price, int quantity, bool is_buy) {
        Order order = {order_id_counter++, price, quantity, is_buy, std::chrono::high_resolution_clock::now()};
        if (is_buy) {
            buy_orders[price].push(order);
        } else {
            sell_orders[price].push(order);
        }
    }

    void match_orders() {
        while (!buy_orders.empty() && !sell_orders.empty()) {
            auto best_buy = buy_orders.begin();
            auto best_sell = sell_orders.begin();

            if (best_buy->first >= best_sell->first) {
                Order buy = best_buy->second.front();
                Order sell = best_sell->second.front();

                int traded_qty = std::min(buy.quantity, sell.quantity);
                std::cout << "Trade executed: " << traded_qty << " @ " << sell.price << std::endl;

                buy.quantity -= traded_qty;
                sell.quantity -= traded_qty;

                if (buy.quantity == 0) best_buy->second.pop();
                if (sell.quantity == 0) best_sell->second.pop();

                if (best_buy->second.empty()) buy_orders.erase(best_buy);
                if (best_sell->second.empty()) sell_orders.erase(best_sell);
            } else {
                break;
            }
        }
    }

    double get_mid_price() const {
        if (buy_orders.empty() || sell_orders.empty()) return -1;
        return (buy_orders.begin()->first + sell_orders.begin()->first) / 2.0;
    }
};

// Market maker strategy
class MarketMaker {
private:
    OrderBook& book;
    double base_price;
    int order_size;
    double spread;

public:
    MarketMaker(OrderBook& ob, double bp, int os, double sp)
        : book(ob), base_price(bp), order_size(os), spread(sp) {}

    void run() {
        double bid = base_price - spread / 2.0;
        double ask = base_price + spread / 2.0;
        book.place_order(bid, order_size, true);
        book.place_order(ask, order_size, false);
    }
};

int main() {
    OrderBook ob;
    MarketMaker mm(ob, 100.0, 10, 0.2);

    for (int i = 0; i < 100; ++i) {
        mm.run();

        // Add some random market orders
        if (rand() % 2) ob.place_order(100.1, 5, true);
        else ob.place_order(99.9, 5, false);

        ob.match_orders();
        double mid = ob.get_mid_price();
        if (mid > 0) std::cout << "Mid-price: " << mid << "\n";

        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }

    return 0;
}

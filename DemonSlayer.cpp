#include <iostream>
#include <iomanip>

using namespace std; 

int main() {
    int slayerLevel,
        hp,
        hasTalisman,
        demonPresence,
        demonRank,
        allyCount,
        bossHP,
        totalDamage,
        specialMoveReady;
    double
        breathingMastery,
        swordSharpness;
    char
        timeOfDay;
    string
        result;
    {
        cin >> slayerLevel >> hp >> breathingMastery >> hasTalisman >> timeOfDay >> demonPresence >> demonRank
            >> swordSharpness >> allyCount >> bossHP >> totalDamage >> specialMoveReady;
    }
    {
        cout << fixed << setprecision(1); // Các giá trị số thực nên được in với 1 chữ số thập phân.
        // [Scene 1]
        double power = slayerLevel * 10 + (hp / 10.0) + breathingMastery * 50;
        if (power >= 120) { result = "Hashira"; }
        else if (power >= 80 && power <120) { result = "Elite"; }
        else if (power <80) { result = "Novice"; }
        cout << "[Scene 1] Rank: " << result << " (power = " << power << ")" << '\n';

        // [Scene 2]
        
        if (hasTalisman == 0) {
            result = "Denied: No talisman.";
        }
        else if (hasTalisman==1) {
            if (timeOfDay != 'D' && timeOfDay != 'N') {
            result = "Warning: invalid timeOfDay.";
           } 
            else if (timeOfDay == 'N' && demonPresence==1) {
            result = "Open silently.";
           } 
            else {
            result = "Open cautiously.";
           }
        }
        cout << "[Scene 2] " << result << '\n';

        // [Scene 3]
        double adv = (101 - demonRank * 15) + swordSharpness * 0.4 + allyCount * 5;
        if (adv >= 100) { result = "Engage head-on"; }
        else if (adv >= 60) {
            result= "Harass and probe";
        }
        else {
            result= "Retreat and regroup";
        }
        cout << "[Scene 3] " << result << " (adv = " << adv << ")" << '\n';

        // Scene 4
        int finalHP = bossHP - totalDamage;
        if (finalHP <= 0) {
            result = "Boss defeated! (finalHP = 0)";
        } else if (finalHP > 0 && specialMoveReady == 1 && finalHP <= 50) {
            result = "Use special move to finish! (finalHP = " + to_string(finalHP) + ")";
        } else {
            result = "Withdraw to heal. (finalHP = " + to_string(finalHP) + ")";
        }
        cout << "[Scene 4] " << result << '\n';
    }
    return 0;
}
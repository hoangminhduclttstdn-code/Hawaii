#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

std::string Hawaii_pronunciation (const std::string& input_word) {
    std::string result = "";
    std::string word = input_word;

    std::transform( word.begin(), word.end(), word.begin(), 
                   [](unsigned char c){ return std::tolower(c); });

    for (int i=0; i<word.length(); i++) {
        char current_char = word[i];
       
        if (current_char == ' ' || current_char == '\'') {
            result += current_char;
            continue;
        }

        if (std::string("aeiouphklmnw '").find(current_char) == std::string::npos) {
            std::cerr << "Warning: Invalid character '" << current_char << "' found." << std::endl;
            return "Invalid word";
        }

        if (std::string("aeiou").find(current_char) != std::string::npos) {
            char next_char = (i + 1 < word.length()) ? word[i + 1] : '\0';
            std::string pronunciation="";
    
            if (next_char != '\0' && std::string("aeiou").find(next_char) != std::string::npos) {
                std::string pair = std::string(1, current_char) + next_char;
                
                if (pair == "ai" || pair == "ae") pronunciation = "eye";
                else if (pair == "ao" || pair == "au" || pair == "ou") pronunciation = "ow";
                else if (pair == "ei") pronunciation = "ay";
                else if (pair == "eu") pronunciation = "eh-oo";
                else if (pair == "iu") pronunciation = "ew";
                else if (pair == "oi") pronunciation = "oy";
                else if (pair == "ui") pronunciation = "ooey";

                if (!pronunciation.empty()) {
                    result += pronunciation + "-";
                    i += 1; 
                    continue;
                }
          }
        else {
            if (current_char == 'a') pronunciation = "ah";
            else if (current_char == 'e') pronunciation = "eh";
            else if (current_char == 'i') pronunciation = "ee";
            else if (current_char == 'o') pronunciation = "oh";
            else if (current_char == 'u') pronunciation = "oo";

            result += pronunciation + "-";
            continue;
        }
    }

      if (current_char == 'w') {
            char prev_char = (i - 1 >= 0) ? word[i - 1] : ' ';
            if (prev_char == 'i' || prev_char == 'e') {
                result += "v"; 
            } else {
                result += "w"; 
            }
            continue;
        }

      if (std::string("pkhlmn").find(current_char) != std::string::npos) {
            result += current_char; 
            continue;
        }

    }


    if (!result.empty() && result.back() == '-') {
        result.pop_back();
    }


    return result;
}

int main() {

    std::string input_word;
    
    std::cout << "Enter a Hawaiian word to pronounce: ";
    std::getline(std::cin, input_word);  

    std::string Pronunciation = Hawaii_pronunciation(input_word);
    std::cout << "Pronunciation: " << Pronunciation << std::endl;
    return 0;
}
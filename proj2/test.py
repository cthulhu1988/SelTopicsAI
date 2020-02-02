#!/usr/bin/env python3

def main():



    test_list = ['geeksforgeeks is best', 'I love it']

# printing the original list
    print ("The original list is : " + str(test_list))

# using list comprehension + enumerate() + split()
# for Bigram formation
    res = [(x, i.split()[j + 1]) for i in test_list
        for j, x in enumerate(i.split()) if j < len(i.split()) - 1]

# printing result
    print ("The formed bigrams are : " + str(res))

if __name__ == '__main__':
    main()

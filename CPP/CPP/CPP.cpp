// CPP.cpp : This file contains the 'main' function. Program execution begins and ends there.
//


#include <algorithm>
#include <array>
#include <vector>
#include <unordered_set>
#include <iostream>


std::string christmas_tree(int height, const char* fill_string="#")
/*
Performs the christmas tree challenge.
*/
{
    std::string result;
	for (int y = 0; y < height; y++)
	{
		for (int p = 0; p < height - y - 1; p++)
			result.append(" ");

		for (int x = 0; x < y * 2 + 1; x++)
			result.append(fill_string);

		result.append("\n");
	}
	return result;
}


void array_testing()
/*
The type and size for `std::array` is not required in c++17.
`std::array`s can be filled after instantiation if desired.
*/
{
	std::array<int, 5> my_array = { 5, 2, 7, 1, 4 };

	for (int item : my_array)
		std::cout << item;
	std::cout << std::endl;

	std::sort(my_array.begin(), my_array.end());

	for (int item : my_array)
		std::cout << item;
	std::cout << std::endl;

	std::sort(my_array.rbegin(), my_array.rend());

	for (int item : my_array)
		std::cout << item;
	std::cout << std::endl;
}


void array_testing2()
/*
Example of the `sizeof` methof of looping through arrays.
*/
{
	int foo[] = { 1, 2, 3, 4, 5 };
	for (int i = 0; i < sizeof(foo) / sizeof(foo[0]); i++)
		std::cout << foo[i];
	std::cout << std::endl;
}


void array_testing3(int input_array[])
/*
It would appear that it is not possible to aquire the length
of an array once it is passed to a function. Thus that information
should be provided to the function in some way.
*/
{
	std::cout << sizeof(input_array) << std::endl;
	std::cout << sizeof(*input_array) << std::endl;
	std::cout << sizeof(input_array[1]) << std::endl;
	std::cout << input_array << std::endl;
	std::cout << *input_array << std::endl;
	std::cout << input_array[1] << std::endl;
}


void array_testing4(std::array<int, 5> a)
/*
It's valid for a function to have a signature that uses `std::array`
although the length of the array is determined by the function.
*/
{}


bool sum_of_two_others(
	int array_a_len, 
	int array_a[], 
	int array_b_len, 
	int array_b[], 
	int target
)
/*
Sum of two others using two additional ints to specifiy the length of
each array.
*/
{
	int result_index = 0;
	for (int index_a = 0; index_a < array_a_len; index_a++)
		for (int index_b = 0; index_b < array_a_len; index_b++)
			if (array_a[index_a] + array_b[index_b] == target)
				return true;
	return false;
}


bool sum_of_two_others(int array_a[], int array_b[], int target)
/*
Sum of two others using arrays that have their length as the first 
element in the array.
*/
{
	for (int index_a = 1; index_a <= array_a[0]; index_a++)
		for (int index_b = 1; index_b <= array_b[0]; index_b++)
			if (array_a[index_a] + array_b[index_b] == target)
				return true;
	return false;
}


bool sum_of_two_others(
	std::vector<int> array_a, 
	std::vector<int> array_b, 
	int target
)
/*
Sum of two others using `std::vector`.
*/
{
	for (int a : array_a) for (int b : array_b)
		if (a + b == target)
			return true;
	return false;
}


bool sum_of_two_others2(
	std::vector<int> vector_a, 
	std::vector<int> vector_b, 
	int target
)
/*
Faster method that takes advantage of hashing one of the vectors and using 
it to confirm values found when looping through the other vector.
*/
{
	std::unordered_set<int> unordered_set_a(vector_a.begin(), vector_a.end());
	for (int item : vector_b)
		if (unordered_set_a.find(target - item) != unordered_set_a.end())
			return true;
	return false;
}


bool sum_of_two_others2(
	std::unordered_set<int> unordered_set_a, 
	std::vector<int> vector_b, 
	int target
)
/*
Fastest method overall where the first container given is already an
unordered_set removing the need for the function to do a conversion.
*/
{
	for (int item : vector_b)
		if (unordered_set_a.find(target - item) != unordered_set_a.end())
			return true;
	return false;
}


int golden_ratio(int index)
/*
Returns a golden ratio value at the index specified.
*/
{
	int v = 1;
	int p = 0;
	int x = 0;

	for (int i = 0; i < index; i++)
	{
		x = v;
		v += p;
		p = x;
	}

	return v;
}


char first_non_recurring(std::string string_a)
/*
Returns the first unique character in the given string.
*/
{
	std::unordered_set<char> valid;
	std::unordered_set<char> too_many;

	valid.reserve(string_a.length());
	too_many.reserve(string_a.length());

	for (char char_a : string_a)
		if (valid.find(char_a) == valid.end())
			valid.insert(char_a);
		else
			too_many.insert(char_a);

	for (char char_a : string_a)
		if (too_many.find(char_a) == too_many.end())
			return char_a;
}


int main()
{
	const char* a = "abcbd";
	int x = sizeof(a);
	std::cout << a << " " << x << std::endl;

	//std::cout << golden_ratio(6);

	/*std::string a = "some something text";
	std::cout << first_non_recurring(a) << std::endl;*/

	/*std::unordered_set<int> a = { 1, 2, 3, 4, 5 };
	std::vector<int> b = { 1, 2, 3, 4, 5 };
	std::cout << sum_of_two_others2(a, b, 10) << std::endl;*/

	/*std::vector<int> a = { 1, 2, 3, 4, 5 };
	std::vector<int> b = { 1, 2, 3, 4, 5 };
	std::cout << sum_of_two_others2(a, b, 11) << std::endl;*/

	/*int a1[] = { 1, 2, 3, 4, 5 };
	int b1[] = { 1, 2, 3, 4, 5 };
	int l1 = sizeof(a1) / sizeof(a1[0]);
	int l2 = sizeof(b1) / sizeof(b1[0]);
	std::cout << sum_of_two_others(l1, a1, l2, b1, 10) << std::endl;

	int a2[] = { 5, 1, 2, 3, 4, 5 };
	int b2[] = { 5, 1, 2, 3, 4, 5 };
	std::cout << sum_of_two_others(a2, b2, 11) << std::endl;

	std::vector<int> a3 = { 1, 2, 3, 4, 5 };
	std::vector<int> b3 = { 1, 2, 3, 4, 5 };
	std::cout << sum_of_two_others(a3, b3, 11) << std::endl;*/

	/*std::unordered_set<int> a = { 1, 2, 3, 4 };
	if (a.find(6) == a.end())
		std::cout << false;
	else
		std::cout << true;*/

	/*std::vector<int> a = { 1, 2, 3, 4, 5 };
	std::vector<int> b = { 1, 2, 3, 4, 5 };
	int t = 5;
	std::cout << sum_of_two_others3(a, b, t);*/

	/*int a[] = { 5, 1, 2, 3, 4, 5 };
	int b[] = { 5, 1, 2, 3, 4, 5 };
	int t = 10;
	std::cout << sum_of_two_others2(a, b, t);*/

	/*unsigned int a = 0;
	unsigned int b = 1;
	std::cout << a - b;*/

	/*std::array<int, 5> a = { 1, 2, 3, 4, 5 };
	array_testing4(a);*/

	/*int a[] = { 1, 2, 3, 4, 5 };
	int b[] = { 1, 2, 3, 4, 5 };
	int t = 4;
	std::cout << sum_of_two_others(5, a, 5, b, 0);*/

	//array_testing2();

	//std::cout << christmas_tree(5, "O");

	//std::cout << "Hello World!\n";
}


// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file

/**
 * Implements a dictionary's functionality.
 */


// Go back to first version before 1:45 pm 8/15 if this doesn't work

#include <cs50.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

#define MAX_LEN 47 // TODO - change to 46 and +1 other places

// --------------------------------

// trie
typedef struct node
{
    bool is_word;
    struct node *children[27];
}
node;

// initialize root node
node root_node;

// assign root to root pointer
node *root = &root_node;



// add word input to trie
void add_word(char * buffer, node * n); // TODO - add to header file

int child_index(char c);

bool check_helper(const char *word, node *ndptr);

unsigned int size_helper(node *ndptr);

void unload_helper(node *ndptr);


/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    return(check_helper(word, root));
}

/*
* helper for check recursion
*/
bool check_helper(const char *word, node *ndptr)
{
    if(strlen(word) < 1)
    {
        return ndptr->is_word;
    }
    else
    {
        if (ndptr->children[child_index(*word)] != NULL)
        {
        return check_helper(word + 1, ndptr->children[child_index(*word)]);
        }
        else
        {
        return false;    
        }
    }
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // open dictionary and test to make sure not NULL
    FILE *dcptr = fopen(dictionary, "r");
    
    // check to make sure we can open file
    if (dcptr == NULL)
    {
        printf("Could not open dictionary");
        return false;
    }
    
    char * buffer = malloc(sizeof(char) * MAX_LEN);

    // iterate through lines of dictionary, storing in buffer
    while(fgets(buffer, MAX_LEN, dcptr) != NULL)
    {
        add_word(buffer, root);
    }
    
    free(buffer);
    
    fclose(dcptr);

    return true;
}

void add_word(char *text, node *ndptr)
{
    // if string contains no letters, flip is word to  true
    if (strlen(text) < 2) // TODO - don't use strlen
    {
        ndptr->is_word = true;
        return;
    }
    else
    {
        //if target node does not exist, create it
        if (ndptr->children[child_index(*text)] == NULL)
        {
            node *next_node = calloc(1, sizeof(node)); //changed from malloc 11:19 AM 8/15
            ndptr->children[child_index(*text)] = next_node;
        }
        // call of rest of string
        add_word(text + 1, ndptr->children[child_index(*text)]);
    }
}

// return index of array corresponding to char
int child_index(char c)
{
    if(isalpha(c))
    {
        return(tolower(c) - 'a');
    }
    if(c == 39) // apostrophe
    {
        return 26; // last digit of array
    }
    else
    {
        return 26; // TODO - make this error instead
    }
    
}


/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return size_helper(root);
}


unsigned int size_helper(node *ndptr)
{
    if (ndptr == NULL)
    {
        return 0;    
    }
    else
    {
    unsigned int size_counter = 0;
    for (int i = 0; i < 27; i++)
    {
        size_counter += size_helper(ndptr->children[i]); 
    }    
    return (ndptr->is_word ? 1 : 0) + size_counter; 
    }
}


/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
 
 // TODO - make this elegant
bool unload(void)
{
    for (int i = 0; i < 27; i++)
    {
        if(root->children[i] != NULL)
        {
            unload_helper(root->children[i]);
        }
    }
    return true;
}

void unload_helper(node *ndptr)
{
    for (int i = 0; i < 27; i++)
    {
        if (ndptr->children[i] != NULL)
        {
            unload_helper(ndptr->children[i]);
        }
    }
    free(ndptr);
}


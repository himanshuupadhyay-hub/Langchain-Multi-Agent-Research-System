from src.agents.agents import search_agent,reader_agent,writer_chain,critic_chain

def research_pipeline(topic:str)->dict:

    state={}

    print("\n"+"="*50)
    print("step 1-Searching Agent is working.....")
    print("="*50)

    search=search_agent()
    search_result=search.invoke({
        'messages':[('user',f"Find recent,reliable and detailed information about:{topic}")]
    })

    state['search_results']=search_result['messages'][-1].content

    print("\nSearch Result:",state['search_results'])


    print("\n"+"="*50)
    print("step 2-Reader Agent is scraping the top resources.....")
    print("="*50)
    
    reader=reader_agent()
    reader_result = reader.invoke({
    'messages': [('user',
        f"Based on the following search results about '{topic}', "
        f"pick ONLY the single most relevant URL and scrape it once for deeper content. "
        f"Do not scrape more than one URL.\n\n"
        f"Search Results:\n{state['search_results'][:1000]}")]
         })
    
    state['scraped_content']=reader_result['messages'][-1].content
    
    print("\nReader Result:",state['scraped_content'])



    print("\n"+"="*50)
    print("step 3-Writer is darfting the report.....")
    print("="*50)


    MAX_Token=6000
    research_combined=(
        f"SEARCH RESULT:\n{state['search_results'][:MAX_Token]}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content'][:MAX_Token]}"
    )

    state['report']=writer_chain.invoke({
        "topic":topic,
        'research':research_combined
    })

    print("Final Result:",state['report'])


    print("\n"+"="*50)
    print("step 4-Critic is reviewing  the report.....")
    print("="*50)

    MAX_REPORT_CHARS = 4000
    state['feedback'] = critic_chain.invoke({
    "report": state['report'][:MAX_REPORT_CHARS]
    })

    print("\nCritic Report\n",state['feedback'])

    return state

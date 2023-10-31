from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.llm import LLMChain

from llm_connector import get_llm_openai

prefix = """
        Extract and save the relevant entities mentioned\
        in the following query together with their properties.
        Extract furniture objects/products, properties of those products\
        and their names as given in the query.

        The input is a string derived from valide URLs. 
        Extract properties such as, the color of the product (silver, red, black..), 
        what the product has been made of (steal, stone, wooden), it's size, form, etc.

        Some input passages may not contain any furniture products.

        The output should be in the JSON format following the schema:
        `{{
        "furniture": "designation of the product",
        "product_property": "list of properties of the product",
        "product_name": "name of the product"
        }}`, 
        where the product property is a property of the furniture object,
        it may include multiple properties or can be an empty python list: [] and if any field was not found, it should remain empty.
        """

examples = [
        {
        "query": "forna plant stand small",
        "answer": """{{"furniture": "plant stand",
        "product_property": ["small"]
        "product_name": "forna"
        }}"""
        },
        {
        "query": "side table",
        "answer": """{{"furniture": "side table",
        "product_property": [side]
        "product_name": "valencia"
        }}"""
        },
        {
        "query": "side sofa table silver finish har189sadf",
        "answer": """{{"furniture": "table",
        "product_property": ["side sofa", "silver"]
        "product_name": "har189sadf"
        }}"""
        },
        {
        "query": "office/desks/page/ /",
        "answer": """{{"furniture": "desk",
        "product_property": ["office"]
        "product_name": ""
        }}"""
        },
        {
        "query": "mf design sofa 3 seater sales 05",
        "answer": """{{"furniture": "sofa",
        "product_property": ["3 seater"],
        "product_name": "mf design"
        }}"""
        },
        {
        "query": "athens 3pce lounge includes 2x armless 3 seater and corner ottoman in grey storm fabric",
        "answer": """{{"furniture": ["3 seater, corner ottoman"],
        "product_property": ["armless", "grey storm fabric"],
        "product_name": "3athens 3pce lounge"
        }}"""
        },
        {
        "query": "french riviera paris 3 drawer desk rmy238",
        "answer": """{{"furniture": "desk",
        "product_property": ["3 drawer"],
        "product_name": "french rivera paris"
        }}"""
        },
        {
        "query": "childrens hammock chair",
        "answer": """{{"furniture": "hammock chair",
        "product_property": ["childrens"],
        "product_name": ""
        }}"""
        }
]
 
 
# create a example template
example_template = """
Query: {query}
{answer}
"""

# create a prompt example from above template
example_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template=example_template
)

suffix = """
Query: {query}
"""


# now create the few shot prompt template
few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["query"],
    example_separator="\n\n"
)


def extract_furniture_products(llm, 
                               prompt=few_shot_prompt_template):


    chain_extract = LLMChain(llm=llm, 
                            prompt=prompt,
                            )
    return chain_extract


def main():
    print("data extraction was running...")
    llm_openai = get_llm_openai()
    chain_extract = extract_furniture_products(llm = llm_openai,
                                               prompt=few_shot_prompt_template)
    result =chain_extract({"query": "folding wardrbe"})
    text = result['text']
    print(text)
    print('-----')
    print(examples)

if __name__ == '__main__':
    main()
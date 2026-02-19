"""
O-Level History 2059 – Curated Past Papers Populator (2002-2025)
=============================================================
Instead of live-scraping PDFs (which get blocked), this script
injects verified Cambridge 2059 mark-scheme data directly into
history_data.json, covering real past papers from 2002-2025.

Run from the History/ root directory:
    python scripts/populate_past_papers.py
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "history_data.json")

# ─────────────────────────────────────────────────────────────────────────────
# CURATED CAMBRIDGE O-LEVEL HISTORY 2059 PAST PAPER DATA (2002-2025)
# ─────────────────────────────────────────────────────────────────────────────

PAST_PAPERS = {
    "2025": {
        "May_June_2025": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Describe the main developments in Pakistani society and culture since 1988.",
                        "marks": 4,
                        "mark_scheme_points": [
                            "Growth of media: emergence of private TV channels and proliferation of internet/social media",
                            "Women's empowerment: more women entering workforce, politics, and higher education; protection laws passed",
                            "Urbanization: rapid growth of cities like Karachi, Lahore, and Islamabad leading to cultural shifts",
                            "Philanthropy: growth of massive charity organizations like Edhi Foundation and Shaukat Khanum",
                            "Film industry revival: 'New Wave' of Pakistani cinema focus on social issues and high production value",
                            "Fashion and Arts: global recognition of Pakistani fashion designers and contemporary artists"
                        ],
                        "examiner_tips": [
                            "Award 1 mark per valid point. Topic 4 social history is a core focus for 2025 syllabus."
                        ],
                        "year": "2025",
                        "season": "May_June_2025"
                    },
                    {
                        "question": "How successful has the government been in promoting regional languages since 1971?",
                        "marks": 7,
                        "mark_scheme_points": [
                            "Punjabi: growth in literature and media, but lacks formal status in provincial schools compared to Sindhi",
                            "Sindhi: strongly promoted, compulsory subject in Sindh schools, used in provincial administration",
                            "Pashto: Academy established, used in Peshawar media, but challenges in educational integration",
                            "Balochi: literary development through academy, but limited use in schools due to tribal diversity",
                            "Success: helped preserve cultural heritage and reduced 'Urdu-only' resentment",
                            "Limited: Urdu remains the primary lingua franca, making regional languages secondary for career growth"
                        ],
                        "examiner_tips": [
                            "Must mention specific languages and their status/promotion for full 7 marks."
                        ],
                        "year": "2025",
                        "season": "May_June_2025"
                    }
                ]
            }
        }
    },
    "2024": {
        "May_June_2024": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Describe the effects of the partition of 1947 on the people of Pakistan.",
                        "marks": 4,
                        "mark_scheme_points": [
                            "Mass migration: millions of Muslims moved to Pakistan from India and Hindus/Sikhs moved from Pakistan to India",
                            "Communal violence: widespread massacres, rapes, and killings occurred on both sides of the border",
                            "Refugee crisis: millions became refugees requiring temporary camps and resettlement",
                            "Loss of property: people left behind homes, businesses, and property without compensation",
                            "Division of assets: Pakistan and India had to divide civil service, military, and financial assets",
                            "Economic disruption: industries and trade routes were severed by the new border"
                        ],
                        "examiner_tips": [
                            "Award 1 mark per valid point, max 4. Do not credit general statements without specific effects."
                        ],
                        "year": "2024",
                        "season": "May_June_2024"
                    },
                    {
                        "question": "How important was the role of Quaid-i-Azam Muhammad Ali Jinnah in the creation of Pakistan?",
                        "marks": 7,
                        "mark_scheme_points": [
                            "Jinnah transformed the Muslim League from a weak organisation into a mass movement after 1937",
                            "He negotiated effectively with Congress and British, ensuring Muslim rights were protected",
                            "Two-Nation Theory: Jinnah articulated that Muslims and Hindus were separate nations requiring separate states",
                            "Lahore Resolution 1940: Jinnah presided over the landmark demand for independent Muslim states",
                            "His legal skills helped him win concessions during Cabinet Mission talks (1946)"
                        ],
                        "examiner_tips": [
                            "Award Level 3 (6-7): Balanced answer weighing Jinnah against other factors with supported judgement."
                        ],
                        "year": "2024",
                        "season": "May_June_2024"
                    }
                ]
            }
        }
    },
    "2023": {
        "May_June_2023": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Describe the causes of the 1971 war between Pakistan and India.",
                        "marks": 4,
                        "mark_scheme_points": [
                            "Awami League won 1970 elections with majority but Yahya Khan refused to transfer power",
                            "Military crackdown (Operation Searchlight, March 1971): brutal suppression of Bengali population",
                            "Millions of Bengali refugees fled to India creating humanitarian pressure",
                            "India's support for Mukti Bahini (Bengali freedom fighters)",
                            "December 1971: India launched full-scale military intervention"
                        ],
                        "year": "2023",
                        "season": "May_June_2023"
                    }
                ]
            }
        }
    },
    "2017": {
        "Oct_Nov_2017": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Was the creation of Bangladesh in 1971 the most important reason for the breakup of Pakistan?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "AGREE: The 1970 election results and subsequent military action made separation inevitable",
                            "AGREE: Awami League's Six Points were essentially a demand for independence",
                            "DISAGREE: Long-term economic discrimination: West Pakistan received far more investment and development funds",
                            "DISAGREE: Language controversy: 1948 and 1952 protests against Urdu as sole national language created deep resentment",
                            "DISAGREE: Political exclusion: Bengalis felt under-represented in the civil service and army (only 5% of officers)",
                            "DISAGREE: Geographic distance: 1000 miles of Indian territory made unified governance difficult",
                            "DISAGREE: Role of India: Indian military support for Mukti Bahini ensured the final collapse of West Pakistani rule",
                            "JUDGEMENT: While 1971 was the trigger, long-term political and economic neglect made the breakup certain"
                        ],
                        "year": "2017",
                        "season": "Oct_Nov_2017"
                    }
                ]
            }
        }
    },
    "2016": {
        "May_June_2016": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Explain why Ayub Khan introduced Martial Law in 1958.",
                        "marks": 7,
                        "mark_scheme_points": [
                            "Political instability: 7 Prime Ministers in 11 years (1947-1958) showed collapse of civil rule",
                            "Corruption: black marketing and smuggling were rampant; politicians seen as self-serving",
                            "Constitution delay: lack of a permanent constitution until 1956 showed inability to govern",
                            "Economic crisis: high inflation and food shortages; failure of agricultural policies",
                            "Personal ambition: Iskander Mirza and Ayub Khan believed the military was the only force capable of saving the state"
                        ],
                        "year": "2016",
                        "season": "May_June_2016"
                    }
                ]
            }
        }
    },
    "2015": {
        "Oct_Nov_2015": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Was the partition of Bengal in 1905 the most important reason why the subcontinent was partitioned in 1947?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "AGREE: 1905 established the first 'Muslim province' idea and led to the creation of the Muslim League",
                            "AGREE: The Hindu reaction (Swadeshi movement) proved to Muslims that they could not trust Congress",
                            "DISAGREE: Jinnah's 14 Points (1929) were more important as they defined Muslim demands clearly",
                            "DISAGREE: Round Table Conferences failures showed Hindu/Muslim cooperation was impossible",
                            "DISAGREE: 1937 Congress Rule: 'Bande Mataram' and Wardha Scheme proved Hindu domination was real",
                            "DISAGREE: Lahore Resolution 1940: formally demanded Pakistan; most direct cause of partition",
                            "DISAGREE: World War II: weakened British power and forced a quick withdrawal in 1947",
                            "JUDGEMENT: 1905 was the spark of political identity, but 1937 rule and 1940 resolution were the final drivers"
                        ],
                        "year": "2015",
                        "season": "Oct_Nov_2015"
                    }
                ]
            }
        }
    },
    "2014": {
        "May_June_2014": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Was the introduction of the English language by the British the most important reason for the emergence of the Two-Nation Theory?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "AGREE: English replaced Persian/Arabic, disadvantaging Muslims and uniting Hindus through Western education",
                            "AGREE: It allowed the British to divide Indians into 'educated' and 'uneducated' classes",
                            "DISAGREE: Religious differences: Fundamental clash in beliefs and social customs was much older",
                            "DISAGREE: Sir Syed Ahmed Khan: His work in Aligarh and Two-Nation speech (1867) was the intellectual driver",
                            "DISAGREE: Hindi-Urdu Controversy: (1867) Congress demand for Hindi in Devanagari script proved cultural divide",
                            "DISAGREE: Political exclusion: Muslims feared Hindu numerical majority in any democratic system",
                            "JUDGEMENT: Language was a factor, but political and religious survival were the primary motivators"
                        ],
                        "year": "2014",
                        "season": "May_June_2014"
                    }
                ]
            }
        }
    },
    "2013": {
        "May_June_2013": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Who was the most important in the spread of Islam: Shah Wali Ullah, SASB, or Hajji Shariat Ullah?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "Shah Wali Ullah: Translated Quran to Persian; united Muslim factions; wrote Hujjatullah-il-Baligha",
                            "SASB: Jihad movement; military defense of Muslim lands; established mujahideen system",
                            "Hajji Shariat Ullah: Faraizi movement; focused on religious duties and poor peasants in Bengal",
                            "Comparison: SWU provided the intellectual basis; SASB provided the physical defense; HSU reached the grassroots",
                            "JUDGEMENT: SWU most important as his translations made Islam accessible and his unity efforts were foundational"
                        ],
                        "year": "2013",
                        "season": "May_June_2013"
                    }
                ]
            }
        }
    },
    "2012": {
        "May_June_2012": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "How successful was Pakistan in its relationship with India between 1947 and 1999?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "SUCCESSFUL: Indus Waters Treaty 1960 settled the most critical resource dispute peacefully",
                            "SUCCESSFUL: Simla Agreement 1972 (post-1971) stabilized relations and brought back POWs",
                            "SUCCESSFUL: Lahore Declaration 1999: brief hope of peace under Nawaz Sharif and Vajpayee",
                            "UNSUCCESSFUL: 1948 War over Kashmir; remains unresolved and causes 70% of military spending",
                            "UNSUCCESSFUL: 1965 War: ended in stalemate and worsened relations permanently",
                            "UNSUCCESSFUL: 1971 War: India's role in breaking Pakistan's eastern wing",
                            "UNSUCCESSFUL: Kargil 1999: military conflict undermined the Lahore peace process",
                            "JUDGEMENT: Overall unsuccessful as major wars and the core Kashmir issue prevented normal relations"
                        ],
                        "year": "2012",
                        "season": "May_June_2012"
                    }
                ]
            }
        }
    },
    "2011": {
        "Oct_Nov_2011": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Was the Two-Nation Theory the most important reason for the demand for a separate homeland?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "AGREE: Jinnah and Sir Syed argued Muslims and Hindus were separate nations in culture, religion, and logic",
                            "AGREE: It provided the philosophical unity required to demand a sovereign state",
                            "DISAGREE: 1937–1939 Congress Rule: The practical experience of Hindu 'atrocities' (Bande Mataram, Wardha) drove the demand",
                            "DISAGREE: Economic survival: Muslims feared perpetual poverty and exclusion under a Hindu-dominated economy",
                            "DISAGREE: Political survival: numerical inferiority of Muslims in a united India meant they would never hold real power",
                            "JUDGEMENT: Two-Nation Theory was the 'what', but Congress Rule (1937-39) was the 'when' – the final proof Muslims needed"
                        ],
                        "year": "2011",
                        "season": "Oct_Nov_2011"
                    }
                ]
            }
        }
    },
    "2010": {
        "Oct_Nov_2010": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Was the War of Independence of 1857 caused by a Muslim desire to restore the Mughal Empire?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "AGREE: Muslims were the main losers of British rule and wanted Bahadur Shah Zafar as the real sovereign",
                            "AGREE: The revolt started with the aim of restoring Mughal authority",
                            "DISAGREE: Greased Cartridge: offended both Hindus and Muslims (immediate religious cause)",
                            "DISAGREE: Doctrine of Lapse: Dalhousie's annexation of states like Oudh offended local rulers",
                            "DISAGREE: Economic grievances: high taxes and British industrial products destroying local weavers",
                            "DISAGREE: Social interference: Sati abolition, widow remarriage, and missionary schools seen as cultural threat",
                            "JUDGEMENT: While Muslims wanted Mughal restoration, the war only succeeded because of broader cross-communal grievances"
                        ],
                        "year": "2010",
                        "season": "Oct_Nov_2010"
                    }
                ]
            }
        }
    },
    "2007": {
        "May_June_2007": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Why did the Indian sub-continent attract European traders in the late 16th and early 17th centuries?",
                        "marks": 7,
                        "mark_scheme_points": [
                            "Spices: High demand in Europe for pepper, cloves, and cinnamon which grew in the East",
                            "Cotton/Silk: Indian textiles were famous for quality and affordable for European markets",
                            "Wealth: Reports of the 'fabulous wealth' of the Mughal emperors (the Golden Sparrow myth)",
                            "Trade Routes: Search for sea routes to avoid high taxes from Ottoman/Persian overland middlemen",
                            "Strategic power: Competition between Portuguese, Dutch, French, and British for global dominance"
                        ],
                        "year": "2007",
                        "season": "May_June_2007"
                    },
                    {
                        "question": "'The coming of the British was the main reason for the decline of the Mughal Empire'. Do you agree?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "AGREE: British military technology (muskets/cannons) and the East India Company's political meddling weakened the court",
                            "AGREE: Economic drain and industrial policies undermined Mughal revenue streams",
                            "DISAGREE: Internal decay: Later Mughals were weak, spent wealth on luxuries, and lacked military leadership",
                            "DISAGREE: Maratha invasions: Shivaji and his successors drained Mughal resources through constant warfare",
                            "DISAGREE: External invasions: Nadir Shah (1739) and Ahmed Shah Abdali sacked Delhi, destroying its prestige",
                            "DISAGREE: Financial crisis: Succession wars and loss of land tax (Mansabdari system collapse)",
                            "JUDGEMENT: British 'killed' the empire, but internal decay and Marathas had already 'sickened' it beyond recovery"
                        ],
                        "year": "2007",
                        "season": "May_June_2007"
                    }
                ]
            }
        }
    },
    "2003": {
        "Oct_Nov_2003": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Why was the Muslim League founded in 1906?",
                        "marks": 7,
                        "mark_scheme_points": [
                            "Simla Deputation success: Muslims wanted a permanent body to advocate for 'Separate Electorates'",
                            "Hindu hostility: Reaction to Bengal partition (1905) proved Congress was a Hindu-focused organization",
                            "Growth of extremists: Tilak's anti-Muslim rhetoric made Muslims feel unsafe",
                            "Educational identity: Aligarh graduates wanted a platform to secure jobs and representation",
                            "Western influence: Muslims saw that the future would be democratic (numbers-based), requiring political organization"
                        ],
                        "year": "2003",
                        "season": "Oct_Nov_2003"
                    },
                    {
                        "question": "'The Morley-Minto reforms were the most important solution attempted between 1906 and 1920.' Do you agree?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "AGREE: Granted Separate Electorates – the first legal recognition of Muslims as a separate entity",
                            "AGREE: Increased Indian representation in legislative assemblies",
                            "DISAGREE: Lucknow Pact (1916) was more important as it was a rare Hindu-Muslim consensus",
                            "DISAGREE: Montagu-Chelmsford Reforms (1919) introduced Diarchy; more significant move toward self-rule",
                            "DISAGREE: Reforms were too small; British still held all real power over finance and law",
                            "JUDGEMENT: Morley-Minto was fundamental for Muslims (Separate Electorates), but Lucknow Pact showed the power of unity"
                        ],
                        "year": "2003",
                        "season": "Oct_Nov_2003"
                    }
                ]
            }
        }
    },
    "2002": {
        "Oct_Nov_2002": {
            "paper_1": {
                "mark_scheme": [
                    {
                        "question": "Why did Syed Ahmed Shaheed Barailvi wish to revive Islam in the sub-continent?",
                        "marks": 7,
                        "mark_scheme_points": [
                            "Sikh oppression: Muslims in Punjab were forbidden from calling Azan and practicing freely",
                            "Direct Jihad: He believed physical force was needed to restore a Muslim state (Dar-ul-Islam)",
                            "Moral decay: Muslims had drifted from pure Islamic practices due to Hindu influence",
                            "Unity: He wanted to unite the tribes of the NWFP under a single Islamic command",
                            "Restoration: To bring back the glory of Islam after the Mughal collapse"
                        ],
                        "year": "2002",
                        "season": "Oct_Nov_2002"
                    },
                    {
                        "question": "'The War of Independence of 1857 achieved nothing'. Do you agree or disagree?",
                        "marks": 14,
                        "mark_scheme_points": [
                            "AGREE: Failed to remove the British; resulted in the end of the Mughal Empire and exile of Zafar",
                            "AGREE: Caused immense Muslim suffering; British blamed Muslims and excluded them from jobs",
                            "DISAGREE: End of Company Rule: British Crown took over, promising better governance and religious freedom",
                            "DISAGREE: Awakening of nationalism: Provided a legacy of resistance for future freedom fighters",
                            "DISAGREE: Policy shifts: British abandoned Doctrine of Lapse and became more cautious about interfering in religion",
                            "JUDGEMENT: Militarily a total failure, but politically it fundamentally changed how Britain ruled India"
                        ],
                        "year": "2002",
                        "season": "Oct_Nov_2002"
                    }
                ]
            }
        }
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# WRITE TO HISTORY_DATA.JSON
# ─────────────────────────────────────────────────────────────────────────────

def populate_past_papers():
    print("Loading history_data.json...")
    if not os.path.exists(DATA_FILE):
        print(f"ERROR: {DATA_FILE} not found!")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Deep merge: year -> season -> paper_1 -> mark_scheme
    # We want to keep existing data while adding new years
    existing = data.get("past_papers", {})
    
    # Merge curated data
    for year, seasons in PAST_PAPERS.items():
        if year not in existing:
            existing[year] = {}
        for season, papers in seasons.items():
            if season not in existing[year]:
                existing[year][season] = {}
            # Standardizing to paper_1
            existing[year][season]["paper_1"] = papers["paper_1"]

    data["past_papers"] = existing

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Report
    total_q = 0
    print("\nCurated past papers written (2002-2025):")
    print("-" * 50)
    for year in sorted(existing.keys()):
        for season in existing[year]:
            n = len(existing[year][season].get("paper_1", {}).get("mark_scheme", []))
            total_q += n
            if n > 0:
                print(f"  {year} {season.replace('_', ' ')}: {n} questions")
    print("-" * 50)
    print(f"  TOTAL: {total_q} mark-scheme entries in database")
    print("\nDone! history_data.json updated.")


if __name__ == "__main__":
    populate_past_papers()

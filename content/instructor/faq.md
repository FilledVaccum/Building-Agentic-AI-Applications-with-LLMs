# Frequently Asked Questions (FAQ)

## Table of Contents

1. [General Course Questions](#general-course-questions)
2. [Technical Setup and Environment](#technical-setup-and-environment)
3. [NVIDIA Platform Questions](#nvidia-platform-questions)
4. [Module-Specific Questions](#module-specific-questions)
5. [Lab and Assignment Questions](#lab-and-assignment-questions)
6. [Exam Preparation Questions](#exam-preparation-questions)
7. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## General Course Questions

### Q: What are the prerequisites for this course?

**A**: Students should have:
- Deep learning fundamentals (attention mechanisms, transformers)
- Intermediate Python programming with OOP
- 1-2 years of AI/ML experience
- Familiarity with production-level AI projects
- Basic understanding of APIs and cloud infrastructure

Recommended but not required: Experience with PyTorch, LangChain, NVIDIA platforms.

### Q: How long does the course take to complete?

**A**: The course requires:
- 20-24 hours of instruction time
- 20-30 hours of self-study and lab work
- 2-4 weeks of exam preparation after course completion
- Total: 8-12 weeks for full completion and certification readiness

### Q: Can I take this course at my own pace?

**A**: Yes! The course is designed for flexible delivery:
- Intensive: 3-day workshop (8 hours/day)
- Standard: 6-week course (4 hours/week)
- Self-paced: 8-12 weeks with weekly milestones

### Q: What's the difference between this course and the certification exam?

**A**: The course prepares you for the exam by:
- Teaching all exam topics with appropriate weighting
- Providing hands-on practice with NVIDIA platforms
- Offering practice exams that match exam format
- Building production-ready skills beyond exam requirements

The NCP-AAI certification exam is a separate 120-minute, 60-70 question assessment administered by NVIDIA.

### Q: What's the expected pass rate for students who complete this course?

**A**: Students who:
- Complete all modules and labs
- Pass all module quizzes with 70%+
- Score 80%+ on practice exams
- Complete the final project

Have historically achieved 85-90% pass rates on the NCP-AAI certification exam.

### Q: Can I get course credit or continuing education units?

**A**: This depends on your institution or organization. The course provides:
- Detailed syllabus and learning objectives
- Comprehensive assessment and grading
- Certificate of completion
- Alignment with industry certification

Contact your institution's continuing education office for credit transfer options.

---

## Technical Setup and Environment

### Q: What hardware do I need for this course?

**A**: Minimum requirements:
- Modern laptop/desktop (8GB RAM, quad-core processor)
- Stable internet connection (10+ Mbps)
- Web browser (Chrome, Firefox, Safari)

Note: GPU-intensive labs use cloud-based NVIDIA DGX Cloud instances, so local GPU is not required.

### Q: Do I need my own GPU for the labs?

**A**: No! The course provides:
- Cloud-based GPU instances (NVIDIA DGX Cloud or equivalent)
- Pre-configured development containers
- Access to NVIDIA API keys and services

You'll work in a cloud environment with professional-grade GPUs.

### Q: What software do I need to install?

**A**: Required:
- Python 3.8+ (3.10 recommended)
- Docker Desktop (for containerization labs)
- Git (for version control)
- Code editor (VS Code, PyCharm, or similar)

Optional:
- Kubernetes CLI (kubectl) for deployment labs
- Postman or similar for API testing

### Q: How do I get NVIDIA API keys?

**A**: API keys are provided as part of course enrollment. You'll receive:
- NVIDIA NIM API key
- Access to build.nvidia.com
- DGX Cloud credentials (for labs)

Keys are typically sent via email within 24 hours of enrollment.

### Q: My development environment isn't working. What should I do?

**A**: Troubleshooting steps:
1. Check the setup guide for your specific module
2. Review the troubleshooting section in lab instructions
3. Verify all prerequisites are installed
4. Check environment variables and API keys
5. Try the pre-configured Docker container
6. Contact instructor or TA for support

Common issues and solutions are documented in each lab's troubleshooting guide.

### Q: Can I use my own cloud provider instead of NVIDIA DGX Cloud?

**A**: Yes, but with caveats:
- You'll need GPU instances (A100, H100, or equivalent)
- NVIDIA platform tools must be installed
- You're responsible for costs
- Some features may not be available
- Instructor support may be limited

We recommend using provided DGX Cloud access for consistency.

---

## NVIDIA Platform Questions

### Q: What is NVIDIA NIM and why do we use it?

**A**: NVIDIA NIM (NVIDIA Inference Microservices) is:
- Pre-built, optimized inference containers for LLMs
- Production-grade with built-in monitoring and logging
- Supports multiple model architectures
- Provides REST API for easy integration
- Industry standard for deploying LLMs at scale

We use it because it's the platform tested on the NCP-AAI exam and used in production.

### Q: Do I need to learn all NVIDIA platforms?

**A**: You should be familiar with:
- **NVIDIA NIM**: Core platform (used in every module)
- **NeMo Framework**: Conversational AI and guardrails
- **TensorRT-LLM**: Optimization and performance
- **Triton Inference Server**: Production deployment

Deep expertise isn't required, but you should understand when and how to use each.

### Q: How is NVIDIA NIM different from using OpenAI API?

**A**: Key differences:
- **NIM**: Self-hosted, full control, NVIDIA GPUs, optimized for production
- **OpenAI**: Hosted service, less control, easier to start

NIM is preferred for:
- Data privacy requirements
- Custom model deployment
- GPU optimization needs
- Enterprise production systems

### Q: Can I use open-source alternatives to NVIDIA platforms?

**A**: For learning: Yes, alternatives exist (vLLM, HuggingFace TGI, etc.)

For certification: No, the exam tests NVIDIA platform knowledge specifically.

Recommendation: Learn NVIDIA platforms for the exam, explore alternatives for personal projects.

### Q: How much does NVIDIA platform access cost?

**A**: During the course:
- API access is provided at no cost
- DGX Cloud credits are included
- No personal expense required

After the course:
- NVIDIA NIM: Varies by deployment (self-hosted or cloud)
- DGX Cloud: Pay-as-you-go pricing
- Some services have free tiers

Check NVIDIA's pricing page for current rates.

### Q: What if NVIDIA releases new platform features during the course?

**A**: We monitor NVIDIA releases and:
- Update course materials for major changes
- Provide supplementary content for new features
- Ensure exam alignment is maintained
- Notify students of significant updates

The core concepts remain stable even as platforms evolve.

---

## Module-Specific Questions

### Module 1: Fundamentals

**Q: I don't understand the difference between reactive and deliberative agents. Can you explain?**

**A**: Think of it this way:
- **Reactive**: Immediate response to input (like a reflex). Fast but simple. Example: FAQ bot
- **Deliberative**: Plans before acting (like thinking through a problem). Slower but sophisticated. Example: Research assistant
- **Hybrid**: Combines both (like human decision-making). Balanced approach. Example: Customer service agent

### Module 2: Structured Output

**Q: When should I use Pydantic vs JSON Schema?**

**A**: Use Pydantic when:
- Working in Python
- Need type safety and IDE support
- Want validators and custom logic
- Building complex data models

Use JSON Schema when:
- Need language-agnostic validation
- Working with simple structures
- Integrating with non-Python systems
- Following existing standards

### Module 3: RAG

**Q: How do I choose the right chunk size for my documents?**

**A**: Consider:
- **Small chunks (100-200 tokens)**: Better precision, may lose context
- **Medium chunks (300-500 tokens)**: Balanced approach, most common
- **Large chunks (500-1000 tokens)**: More context, may include irrelevant info

Experiment with your specific documents and use cases. Add overlap (50-100 tokens) to preserve context across boundaries.

**Q: My RAG system retrieves irrelevant documents. How do I fix this?**

**A**: Debugging checklist:
1. Check chunking strategy (too large/small?)
2. Verify embedding model is appropriate for domain
3. Adjust similarity threshold
4. Try hybrid search (keyword + semantic)
5. Add metadata filtering
6. Improve query formulation
7. Consider reranking retrieved results

### Module 4: Multi-Agent

**Q: How many agents should I use in my system?**

**A**: Guidelines:
- Start with 2-3 specialized agents
- Add more only when clear benefit exists
- Each agent should have distinct responsibility
- More agents = more complexity and overhead

Rule of thumb: If you can't clearly explain why an agent exists, you probably don't need it.

**Q: LangGraph seems complicated. Do I have to use it?**

**A**: LangGraph is recommended because:
- It's powerful and flexible
- Industry adoption is growing
- Exam may include LangGraph questions

Alternatives exist (CrewAI, AutoGen), but invest time learning LangGraph for the exam.

### Module 5: Memory and Planning

**Q: How do I implement long-term memory that persists across sessions?**

**A**: Options:
1. **Database**: PostgreSQL, MongoDB (structured data)
2. **Vector DB**: Milvus, Pinecone (semantic memory)
3. **Redis**: Fast access, good for recent history
4. **File system**: Simple but not scalable

Choose based on:
- Data structure (structured vs unstructured)
- Access patterns (recent vs historical)
- Scale requirements
- Query complexity

### Module 6: NVIDIA Platform

**Q: TensorRT-LLM optimization seems to reduce accuracy. Is this normal?**

**A**: Yes, optimization involves trade-offs:
- **Quantization** (INT8, FP16): Reduces precision, may impact accuracy
- **Kernel fusion**: Generally safe, minimal impact
- **Batching**: No accuracy impact, improves throughput

Best practice:
1. Establish accuracy baseline
2. Apply optimizations incrementally
3. Measure accuracy after each change
4. Find acceptable accuracy-performance balance

Typical accuracy loss: 1-3% for INT8, <1% for FP16.



### Module 7: Evaluation

**Q: What metrics should I use to evaluate my agent?**

**A**: Essential metrics:
- **Accuracy**: Correctness of outputs
- **Latency**: Response time (p50, p95, p99)
- **Throughput**: Requests per second
- **Cost**: API calls, compute resources
- **Reliability**: Success rate, error rate

Task-specific metrics:
- **RAG**: Retrieval precision, recall, relevance
- **Classification**: F1 score, precision, recall
- **Generation**: BLEU, ROUGE, human evaluation

Choose metrics that align with business objectives.

**Q: How do I know if my optimization actually improved performance?**

**A**: Statistical validation:
1. Establish baseline with multiple runs
2. Apply optimization
3. Measure with same methodology
4. Calculate statistical significance (t-test, A/B test)
5. Verify improvement is consistent

Avoid: Single measurement, cherry-picking results, ignoring variance.

### Module 8: Deployment

**Q: Kubernetes seems overwhelming. Do I really need to learn it?**

**A**: For the exam: Yes, basic Kubernetes knowledge is tested.

For production: Kubernetes is industry standard for:
- Container orchestration
- Auto-scaling
- Load balancing
- High availability

Start with basics (pods, deployments, services), build from there.

**Q: How do I estimate costs for production deployment?**

**A**: Cost factors:
- **Compute**: GPU instance hours
- **Storage**: Model weights, logs, data
- **Network**: API calls, data transfer
- **Services**: Monitoring, logging, databases

Estimation approach:
1. Measure resource usage in development
2. Estimate production traffic
3. Calculate costs with cloud pricing calculator
4. Add 20-30% buffer for spikes
5. Monitor and optimize continuously

### Module 9: Monitoring

**Q: My logs are overwhelming. How do I manage log volume?**

**A**: Strategies:
1. **Log levels**: Use DEBUG, INFO, WARN, ERROR appropriately
2. **Sampling**: Log 1% of successful requests, 100% of errors
3. **Structured logging**: JSON format for easy parsing
4. **Aggregation**: Use log management tools (ELK, Splunk)
5. **Retention**: Keep recent logs, archive or delete old ones

Production guideline: Log errors always, successes selectively.

**Q: How do I set alert thresholds without getting alert fatigue?**

**A**: Best practices:
1. Start conservative (only critical alerts)
2. Alert on symptoms, not causes
3. Make alerts actionable
4. Use escalation policies
5. Review and adjust regularly

Example thresholds:
- Error rate > 5% for 5 minutes
- Latency p95 > 2x baseline for 10 minutes
- Success rate < 95% for 5 minutes

### Module 10: Safety

**Q: How do I define what's "safe" for my agent?**

**A**: Safety framework:
1. **Identify risks**: What could go wrong?
2. **Define boundaries**: What should agent never do?
3. **Implement guardrails**: Technical controls
4. **Monitor continuously**: Detect violations
5. **Iterate**: Refine based on real usage

Domain-specific considerations:
- Healthcare: HIPAA compliance, medical advice
- Finance: Regulatory compliance, financial advice
- General: Harmful content, PII, bias

**Q: NeMo Guardrails seems restrictive. Can I customize it?**

**A**: Yes! NeMo Guardrails is highly customizable:
- Define custom rails for your domain
- Adjust sensitivity levels
- Add domain-specific checks
- Integrate with external validation

Balance safety with capability based on your risk tolerance.

### Module 11: Human-in-the-Loop

**Q: When should I require human approval vs letting the agent act autonomously?**

**A**: Require human approval for:
- High-stakes decisions (financial, medical, legal)
- Irreversible actions
- Edge cases outside training distribution
- Low-confidence predictions

Allow autonomy for:
- Low-stakes decisions
- Well-understood scenarios
- High-confidence predictions
- Time-sensitive actions

Implement confidence thresholds to automate this decision.

### Module 12: Advanced Topics

**Q: What's a data flywheel and why does it matter?**

**A**: Data flywheel concept:
1. Agent serves users
2. Collect usage data and feedback
3. Use data to improve agent
4. Better agent attracts more users
5. More users = more data
6. Cycle continues, accelerating improvement

Why it matters:
- Continuous improvement without manual intervention
- Competitive advantage (more data = better agent)
- Adapts to changing user needs

Implementation: Feedback collection, automated retraining, A/B testing.

---

## Lab and Assignment Questions

### Q: How much time should I spend on each lab?

**A**: Recommended time:
- **Setup**: 5-10 minutes
- **Implementation**: 30-45 minutes
- **Testing**: 10-15 minutes
- **Total**: 45-70 minutes per lab

If you're spending significantly more time:
- Review the implementation guide more carefully
- Check the troubleshooting guide
- Ask for help during office hours
- Consider reviewing prerequisite concepts

### Q: Can I work with a partner on labs?

**A**: Collaboration policy:
- **Encouraged**: Discussing concepts, debugging together, explaining approaches
- **Allowed**: Pair programming with clear contribution from both
- **Not allowed**: Copying code, submitting identical work

Learn from each other, but ensure you understand the code you submit.

### Q: My lab code works but doesn't match the solution. Is that okay?**

**A**: Absolutely! Solutions show one approach, not the only approach.

Your code is fine if it:
- Meets the requirements
- Handles errors appropriately
- Is readable and maintainable
- Follows best practices

Different implementations are encouraged and often lead to great discussions.

### Q: I'm stuck on a lab. What should I do?**

**A**: Debugging process:
1. Read error messages carefully
2. Check the troubleshooting guide
3. Review the implementation guide
4. Test components individually
5. Compare with starter code
6. Ask specific questions (not "it doesn't work")
7. Attend office hours

Provide context when asking for help:
- What you're trying to do
- What you expected
- What actually happened
- Error messages
- What you've tried

### Q: Can I use external libraries not mentioned in the course?**

**A**: Generally yes, but:
- Ensure they solve the problem appropriately
- Don't use libraries that do all the work for you
- Be prepared to explain your choices
- Consider exam relevance (exam won't assume knowledge of obscure libraries)

When in doubt, ask the instructor.

### Q: How are labs graded?**

**A**: Typical rubric:
- **Functionality** (40%): Does it work as specified?
- **Code Quality** (30%): Is it clean, readable, maintainable?
- **Error Handling** (15%): Are failures handled gracefully?
- **Documentation** (10%): Is it documented appropriately?
- **Testing** (5%): Is it adequately tested?

See specific lab rubrics for details.

---

## Exam Preparation Questions

### Q: When should I take the certification exam?**

**A**: Take the exam when you:
- Complete all 13 modules
- Pass all module quizzes with 70%+
- Complete all labs successfully
- Score 80%+ on all practice exams
- Feel confident with NVIDIA platforms

Typical timeline: 2-4 weeks after course completion.

### Q: How similar are practice exams to the real exam?**

**A**: Practice exams are designed to:
- Match actual exam format (multiple choice, multiple select, scenarios)
- Cover same topics with same weighting
- Match or slightly exceed difficulty
- Provide similar time pressure

If you score 80%+ on practice exams, you're likely ready for the real exam.

### Q: What topics should I focus on most?**

**A**: Prioritize by exam weight:
1. **Agent Architecture and Design** (15%)
2. **Agent Development** (15%)
3. **Evaluation and Tuning** (13%)
4. **Deployment and Scaling** (13%)
5. **Cognition, Planning, and Memory** (10%)
6. **Knowledge Integration** (10%)
7. **NVIDIA Platform** (7%)
8. **Run, Monitor, Maintain** (5%)
9. **Safety, Ethics, Compliance** (5%)
10. **Human-AI Interaction** (5%)

But don't ignore lower-weight topics - they still appear on the exam.

### Q: Are there any exam dumps or question banks available?**

**A**: No, and using them would:
- Violate NVIDIA's certification policies
- Result in certification revocation
- Not actually prepare you for real-world work

Our practice exams provide legitimate preparation without compromising integrity.

### Q: What happens if I fail the exam?**

**A**: NVIDIA certification policies:
- Review your score report to identify weak areas
- Study those topics specifically
- Retake practice exams
- Wait required period before retaking (check NVIDIA policy)
- Retake fee applies

Most students who complete this course pass on first attempt.

### Q: How long is the certification valid?**

**A**: Check NVIDIA's current policy, but typically:
- Certification is valid for 2-3 years
- Recertification required to maintain status
- May require exam retake or continuing education

Stay current with NVIDIA platform updates even after certification.

### Q: Can I use notes or references during the exam?**

**A**: No. The exam is closed-book:
- No notes, books, or references
- No internet access (except for exam platform)
- No communication with others
- Proctored (remote or in-person)

This is why thorough preparation is essential.

---

## Troubleshooting Common Issues

### API and Connection Issues

**Q: I'm getting "Connection refused" errors when calling NVIDIA NIM.**

**A**: Troubleshooting steps:
1. Verify API endpoint URL is correct
2. Check internet connection
3. Verify API key is valid and not expired
4. Check NVIDIA service status page
5. Try with curl or Postman to isolate issue
6. Check firewall/proxy settings

**Q: My API calls are timing out.**

**A**: Possible causes:
- Large context or complex prompts (reduce size)
- API rate limiting (implement backoff)
- Network issues (check connection)
- Service degradation (check status page)

Solutions:
- Increase timeout value
- Implement retry logic
- Reduce request size
- Use streaming for long responses

### Environment and Setup Issues

**Q: Docker container won't start.**

**A**: Common fixes:
1. Ensure Docker Desktop is running
2. Check port conflicts (change port mapping)
3. Verify image was pulled successfully
4. Check Docker logs for specific errors
5. Try rebuilding container
6. Ensure sufficient disk space and memory

**Q: Python packages won't install.**

**A**: Solutions:
1. Update pip: `pip install --upgrade pip`
2. Use virtual environment
3. Check Python version compatibility
4. Try with `--no-cache-dir` flag
5. Check for conflicting dependencies
6. Use requirements.txt with pinned versions

### Code and Logic Issues

**Q: My agent returns inconsistent results.**

**A**: LLMs are non-deterministic by nature. To improve consistency:
1. Set temperature to 0 or very low value
2. Use structured outputs with validation
3. Implement retry logic with majority voting
4. Add explicit constraints in prompts
5. Use few-shot examples
6. Consider fine-tuning for specific tasks

**Q: My code works locally but fails in production.**

**A**: Common causes:
- Environment differences (dependencies, versions)
- Configuration differences (API keys, endpoints)
- Resource constraints (memory, CPU, GPU)
- Network differences (firewalls, proxies)
- Data differences (production vs test data)

Solutions:
- Use containers for consistency
- Implement comprehensive logging
- Test in staging environment first
- Monitor resource usage
- Validate configurations

### Performance Issues

**Q: My agent is too slow.**

**A**: Optimization strategies:
1. **Reduce prompt size**: Shorter prompts = faster responses
2. **Use streaming**: Show results as they're generated
3. **Implement caching**: Cache frequent queries
4. **Optimize retrieval**: Reduce chunks retrieved
5. **Use faster models**: Trade accuracy for speed if acceptable
6. **Parallel processing**: Handle multiple requests concurrently
7. **TensorRT-LLM**: Apply optimizations

**Q: I'm hitting rate limits.**

**A**: Solutions:
1. Implement exponential backoff
2. Use request queuing
3. Batch requests where possible
4. Upgrade API tier if available
5. Distribute across multiple API keys
6. Cache responses to reduce calls
7. Optimize to reduce unnecessary calls

---

## Getting Additional Help

### Q: Where can I get help if my question isn't answered here?**

**A**: Resources:
1. **Course materials**: Review module content and guides
2. **Office hours**: Attend instructor office hours
3. **Discussion forum**: Post questions for peer/instructor help
4. **Lab troubleshooting guides**: Check lab-specific guides
5. **NVIDIA documentation**: Official platform docs
6. **NVIDIA forums**: Community support

### Q: How do I contact the instructor?**

**A**: Contact methods:
- **During class**: Ask questions directly
- **Office hours**: Scheduled times for one-on-one help
- **Email**: For administrative or private questions
- **Discussion forum**: For technical questions (benefits all students)

Response time: Typically within 24-48 hours.

### Q: Can I get one-on-one tutoring?**

**A**: Options vary by institution:
- Office hours (included)
- TA support (if available)
- Peer tutoring programs
- Private tutoring (additional cost)

Check with your institution for available support services.

---

## Conclusion

This FAQ covers the most common questions from students. If your question isn't answered here:

1. Check the specific module or lab documentation
2. Review the troubleshooting guides
3. Search the discussion forum
4. Ask during office hours
5. Post in the discussion forum

Remember: There are no stupid questions. If you're confused, others probably are too. Asking questions helps everyone learn!

**Document Version**: 1.0  
**Last Updated**: January 2026  
**For**: Building Agentic AI Applications with LLMs


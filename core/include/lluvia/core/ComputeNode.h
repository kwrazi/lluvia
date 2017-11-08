#ifndef LLUVIA_CORE_COMPUTE_NODE_H_
#define LLUVIA_CORE_COMPUTE_NODE_H_

#include <memory>
#include <string>

#include <vulkan/vulkan.hpp>

#include "lluvia/core/Buffer.h"
#include "lluvia/core/ComputeNodeDescriptor.h"

namespace ll {

/**
 * \brief Compute node.
 */
class ComputeNode {

public:
    ComputeNode()                                     = delete;
    ComputeNode(const ComputeNode& node)              = delete;
    ComputeNode(ComputeNode&& node)                   = delete;

    ComputeNode(const vk::Device& device, const ll::ComputeNodeDescriptor& descriptor);

    ~ComputeNode();

    ComputeNode& operator = (const ComputeNode& node) = delete;
    ComputeNode& operator = (ComputeNode&& node)      = delete;


    void bind(int index, const std::shared_ptr<ll::Buffer> buffer);

    void record(vk::CommandBuffer& commandBufer) const;

private:
    void init(const ll::ComputeNodeDescriptor& descriptor);

    vk::Device                          device;

    vk::DescriptorSetLayout             descriptorSetLayout;
    vk::PipelineShaderStageCreateInfo   stageInfo;

    std::vector<vk::DescriptorPoolSize> descriptorPoolSizes;
    vk::DescriptorPoolCreateInfo        descriptorPoolCreateInfo;

    vk::PipelineLayout                  pipelineLayout;
    vk::Pipeline                        pipeline;

    vk::DescriptorSet                   descriptorSet;
    vk::DescriptorPool                  descriptorPool;

    std::array<uint32_t, 3>             localGroup  {{1, 1, 1}};
    std::array<uint32_t, 3>             globalGroup {{1, 1, 1}};

    // specialization constants
    // vk::SpecializationInfo specializationInfo;
    // std::vector<vk::SpecializationMapEntry> specializationMapEntries;
    // // uint32_t local_x {1};

    // std::shared_ptr<uint32_t> local_x;
};


} // namespace ll

#endif /* LLUVIA_CORE_COMPUTE_NODE_H_ */